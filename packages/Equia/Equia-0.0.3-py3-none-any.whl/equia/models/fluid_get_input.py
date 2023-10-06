from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FluidGetInput")


@attr.s(auto_attribs=True)
class FluidGetInput:
    """Input for request fluid information"""

    user_id: str
    access_secret: str
    fluid_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        fluid_id = self.fluid_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
            }
        )
        if fluid_id is not UNSET:
            field_dict["fluidId"] = fluid_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        access_secret = d.pop("accessSecret")

        fluid_id = d.pop("fluidId", UNSET)

        request_fluid_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            fluid_id=fluid_id,
        )

        return request_fluid_input
