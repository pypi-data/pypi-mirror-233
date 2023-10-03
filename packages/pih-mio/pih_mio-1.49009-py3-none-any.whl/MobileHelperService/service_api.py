import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")

from MobileHelperService.api import (
    MobileHelper as Api,
    MobileSession,
    MobileOutput,
    MobileInput,
    MobileUserInput,
    MobileMarkInput,
    InternalInterrupt,
    AddressedInterruption,
    Flags,
    MIO,
    COMMAND_KEYWORDS
)
from pih import A, PIH, Stdin, NotFound, SubscribtionResult
from pih.tools import ParameterList, BitMask as BM, nl, if_else, js, j, b
from pih.rpc_collection import ServiceDescription
from pih.collection import WhatsAppMessage, User
from MobileHelperService.const import SD

from threading import Thread
from collections import defaultdict
from typing import Callable, Any

SC = A.CT_SC

DEFAULT_COUNT: int = 10

# version 0.8

ADMIN_ALIAS: str = "admin"
COUNT_ALIAS: str = "count"


class MobileHelperService:
    _is_admin: bool = False

    @staticmethod
    def is_admin() -> bool:
        host: str = A.OS.host()
        return MobileHelperService._is_admin or A.D.contains(
            host, A.CT_H.DEVELOPER.NAME
        )

    @staticmethod
    def count() -> int:
        return A.SE.named_arg(COUNT_ALIAS)

    NAME: str = "MobileHelper"

    A.U.for_service(SD)

    mobile_helper_client_map: dict[str, Api] = {}

    def __init__(
        self, max_client_count: int | None, checker: Callable[[str], bool] | None = None
    ):
        self.max_client_count: int | None = max_client_count
        self.root: str = PIH.NAME
        self.checker: Callable[[str], bool] | None = checker
        self.service_description: SD = SD
        self.allow_send_to_next_service_in_chain: dict[str, bool] = defaultdict(bool)

    def start(self) -> bool:
        A.SE.add_arg(ADMIN_ALIAS, nargs="?", const="True", type=str, default="False")
        A.SE.add_arg(COUNT_ALIAS, nargs="?", const=1, type=int, default=DEFAULT_COUNT)
        service_desctiption: ServiceDescription | None = (
            A.SRV_A.create_support_service_or_master_service_description(
                self.service_description
            )
        )
        if A.SRV.is_service_as_support(service_desctiption):
            MobileHelperService._is_admin = A.SE.named_arg(ADMIN_ALIAS).lower() in [
                "1",
                "true",
            ]
        else:
            MobileHelperService._is_admin = False
        if not A.D_C.empty(service_desctiption):
            A.SRV_A.serve(
                service_desctiption,
                self.service_call_handler,
                MobileHelperService.service_starts_handler,
            )
            return True

    def create_mobile_helper(
        self,
        sender: str,
        external_flags: int | None = None,
        recipient: str | None = None,
    ) -> Api:
        is_cli: bool = sender == A.D.get(A.CT_ME_WH.GROUP.PIH_CLI)
        if is_cli:
            external_flags = BM.add(external_flags, Flags.CLI)
        stdin: Stdin = Stdin()
        session: MobileSession = MobileSession(sender, external_flags)
        output: MobileOutput = MobileOutput(session)
        session.say_hello(recipient)
        is_admin: bool = is_cli
        if not is_admin:
            try:
                is_admin = A.C_U.by_group(
                    A.R_U.by_telephone_number(sender).data, A.CT_AD.Groups.Admin
                )
            except NotFound as _:
                pass
        input: MobileInput = MobileInput(
            stdin,
            MobileUserInput(),
            MobileMarkInput(),
            output,
            session,
            [None, -1][is_admin],
        )
        api: Api = Api(PIH(input, output, session), stdin)
        if is_cli:
            api.external_flags = external_flags
        return api

    @staticmethod
    def say_good_bye(mobile_helper: Api) -> str:
        mobile_helper.say_good_bye()
        mobile_helper.show_good_bye = None

    def pih_handler(
        self,
        sender: str,
        line: str | None = None,
        sender_user: User | None = None,
        external_flags: int | None = None,
        chat_id: str | None = None,
    ) -> None:
        mobile_helper: Api | None = None
        is_cli: bool = sender == A.D.get(A.CT_ME_WH.GROUP.PIH_CLI)
        while True:
            try:
                if MobileHelperService.is_client_new(sender):
                    A.IW.remove(A.CT.MOBILE_HELPER.POLIBASE_PERSON_PIN, sender)
                    if is_cli or Api.check_for_starts_with_pih_keyword(line):
                        self.allow_send_to_next_service_in_chain[
                            sender
                        ] = self.is_client_stack_full()
                        if not self.allow_send_to_next_service_in_chain[sender]:
                            MobileHelperService.mobile_helper_client_map[
                                sender
                            ] = self.create_mobile_helper(
                                sender, external_flags, chat_id
                            )
                    else:
                        self.allow_send_to_next_service_in_chain[sender] = False
                else:
                    self.allow_send_to_next_service_in_chain[sender] = False
                if sender in MobileHelperService.mobile_helper_client_map:
                    mobile_helper = MobileHelperService.mobile_helper_client_map[sender]
                    if is_cli and not mobile_helper.wait_for_input():
                        if not Api.check_for_starts_with_pih_keyword(line):
                            line = js((COMMAND_KEYWORDS.PIH[0], line))
                    if mobile_helper.do_pih(line, sender_user, external_flags):
                        if mobile_helper.show_good_bye:
                            if A.D.is_none(external_flags) or not BM.has(
                                external_flags, Flags.SILENCE
                            ):
                                MobileHelperService.say_good_bye(mobile_helper)
                break
            except NotFound:
                break
            except InternalInterrupt as interruption:
                if interruption.type == A.CT.MOBILE_HELPER.InteraptionTypes.NEW_COMMAND:
                    line = mobile_helper.line
                    if not Api.check_for_starts_with_pih_keyword(line):
                        MobileHelperService.say_good_bye(mobile_helper)
                        break
                elif interruption.type in (
                    A.CT.MOBILE_HELPER.InteraptionTypes.TIMEOUT,
                    A.CT.MOBILE_HELPER.InteraptionTypes.EXIT,
                ):
                    MobileHelperService.say_good_bye(mobile_helper)
                    break

    def is_client_stack_full(self) -> bool:
        max_client_count: int | None = self.max_client_count
        if A.D.is_none(max_client_count):
            max_client_count = MobileHelperService.count()
        return len(MobileHelperService.mobile_helper_client_map) == max_client_count

    def is_client_new(value: str) -> bool:
        return value not in MobileHelperService.mobile_helper_client_map

    def receive_message_handler(
        self,
        message_text: str,
        sender: str,
        external_flags: int | None = None,
        chat_id: str | None = None,
    ) -> None:
        interruption: AddressedInterruption | None = None
        while True:
            try:
                if A.D_C.empty(interruption):
                    self.pih_handler(
                        sender, message_text, None, external_flags, chat_id
                    )
                else:
                    for recipient_user in interruption.recipient_user_list():
                        recipient_user: User = recipient_user
                        self.pih_handler(
                            recipient_user.telephoneNumber,
                            " ".join([self.root, interruption.command_name]),
                            interruption.sender_user,
                            interruption.flags,
                        )
                    interruption = None
                break
            except AddressedInterruption as local_interruption:
                interruption = local_interruption

    def receive_message_handler_thread_handler(self, message: WhatsAppMessage) -> None:
        self.receive_message_handler(
            message.message, message.sender, None, message.chatId
        )

    def service_call_handler(
        self,
        sc: SC,
        parameter_list: ParameterList,
        subscribtion_result: SubscribtionResult | None,
    ) -> Any:
        if sc == A.CT_SC.send_event:
            if A.D.is_not_none(subscribtion_result) and subscribtion_result.result:
                if subscribtion_result.type == A.CT_SubT.ON_RESULT_SEQUENTIALLY:
                    message: WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(
                        parameter_list
                    )
                    if A.D.is_not_none(message):
                        if (
                            A.D.get_by_value(A.CT_ME_WH_W.Profiles, message.profile_id)
                            == A.CT_ME_WH_W.Profiles.IT
                        ):
                            allow_for_group: bool = not A.D_C.empty(
                                message.chatId
                            ) and message.chatId in [A.D.get(A.CT_ME_WH.GROUP.PIH_CLI)]
                            if A.D.is_none(message.chatId) or allow_for_group:
                                telephone_number: str = if_else(
                                    allow_for_group, message.chatId, message.sender
                                )
                                if allow_for_group:
                                    message.chatId = message.sender
                                    message.sender = telephone_number
                                if A.D.is_none(self.checker) or self.checker(
                                    telephone_number
                                ):
                                    if self.is_client_stack_full():
                                        return True
                                    else:
                                        if (
                                            telephone_number
                                            in self.allow_send_to_next_service_in_chain
                                        ):
                                            del self.allow_send_to_next_service_in_chain[
                                                telephone_number
                                            ]
                                        Thread(
                                            target=self.receive_message_handler_thread_handler,
                                            args=[message],
                                        ).start()
                                        while (
                                            telephone_number
                                            not in self.allow_send_to_next_service_in_chain
                                        ):
                                            pass
                                        return self.allow_send_to_next_service_in_chain[
                                            telephone_number
                                        ]
                                else:
                                    if (
                                        telephone_number
                                        in MobileHelperService.mobile_helper_client_map
                                    ):
                                        del MobileHelperService.mobile_helper_client_map[
                                            telephone_number
                                        ]
                                    return True
            return False
        if sc == A.CT_SC.send_mobile_helper_message:
            self.receive_message_handler(
                " ".join((self.root, parameter_list.next())),
                parameter_list.next(),
                parameter_list.next(),
            )
        return None

    @staticmethod
    def service_starts_handler() -> None:
        A.O.write_line(nl())
        A.O.blue("Configuration:")
        as_admin: bool = MobileHelperService.is_admin()
        with A.O.make_indent(1):
            A.O.value("As admin", str(as_admin))
            if not as_admin:
                A.O.value("Count", str(MobileHelperService.count()))
        A.SRV_A.subscribe_on(
            A.CT_SC.send_event,
            A.CT_SubT.ON_RESULT_SEQUENTIALLY,
            MobileHelperService.NAME,
        )
        if as_admin:
            A.MIO.create_output(A.D.get(A.CT_ME_WH.GROUP.PIH_CLI)).write_line(
                j(
                    (
                        A.CT_V.ROBOT,
                        " ",
                        nl(b("Pih cli запущен...")),
                        "      Версия: ",
                        MIO.VERSION,
                    )
                )
            )
