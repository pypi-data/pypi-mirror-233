import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A

from MobileHelperService.service_api import MobileHelperService


def checker(telephone_number: str) -> bool:
    if not A.D_C.empty(A.SRV.get_support_host_list(A.CT_SR.MOBILE_HELPER)):
        am_i_admin: bool = telephone_number == A.D.get(A.CT_ME_WH.GROUP.PIH_CLI) or (
            A.D.is_not_none(A.CT.TEST.USER)
            and telephone_number == A.D_TN.by_login(A.CT.TEST.USER)
        )
        if MobileHelperService.is_admin():
            return am_i_admin
        return not am_i_admin
    return True


MobileHelperService(None, checker).start()