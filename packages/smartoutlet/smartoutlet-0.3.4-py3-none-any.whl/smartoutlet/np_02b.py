from typing import ClassVar, Dict, cast

from .interface import OutletInterface, param
from .np_0xb import NP0XBOutlet


@param("host", "the hostname or IP address of the NP-02B you are attempting to control")
@param(
    "outlet",
    "the outlet number (between 1-2 inclusive) that you are attempting to control",
)
@param(
    "username", "the administrator username as specified in the NP-02B web interface"
)
@param(
    "password", "the administrator password as specified in the NP-02B web interface"
)
class NP02BOutlet(NP0XBOutlet):
    type: ClassVar[str] = "np-02b"

    def __init__(
        self,
        *,
        host: str,
        outlet: int,
        username: str = "admin",
        password: str = "admin",
    ) -> None:
        super().__init__(host, 2, outlet, username, password)

    @staticmethod
    def deserialize(vals: Dict[str, object]) -> OutletInterface:
        return NP02BOutlet(
            host=cast(str, vals["host"]),
            outlet=cast(int, vals["outlet"]),
            username=cast(str, vals["username"]),
            password=cast(str, vals["password"]),
        )
