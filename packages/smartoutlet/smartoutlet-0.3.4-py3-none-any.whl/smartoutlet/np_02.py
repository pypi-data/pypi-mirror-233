from typing import ClassVar, Dict, cast

from .interface import OutletInterface, param
from .np_0x import NP0XOutlet


@param("host", "the hostname or IP address of the NP-02 you are attempting to control")
@param(
    "outlet",
    "the outlet number (between 1-2 inclusive) that you are attempting to control",
)
@param(
    "community", "the SNMP read/write community as specified in the NP-02 config menu"
)
class NP02Outlet(NP0XOutlet):
    type: ClassVar[str] = "np-02"

    def __init__(
        self,
        *,
        host: str,
        outlet: int,
        # Yes, they only support one community for read and write.
        community: str = "public",
    ) -> None:
        super().__init__(host, 2, outlet, community)

    @staticmethod
    def deserialize(vals: Dict[str, object]) -> OutletInterface:
        return NP02Outlet(
            host=cast(str, vals["host"]),
            outlet=cast(int, vals["outlet"]),
            community=cast(str, vals["community"]),
        )
