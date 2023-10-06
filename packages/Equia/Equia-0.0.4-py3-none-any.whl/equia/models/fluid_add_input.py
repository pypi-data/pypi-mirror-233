from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_fluid import ApiFluid
from ..types import UNSET, Unset

T = TypeVar("T", bound="FluidAddInput")


@attr.s(auto_attribs=True)
class FluidAddInput:
    """Input for added new fluid to database"""

    user_id: str
    access_secret: str
    fluid: Union[Unset, ApiFluid] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        fluid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fluid, Unset):
            fluid = self.fluid.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
            }
        )
        if fluid is not UNSET:
            field_dict["fluid"] = fluid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        access_secret = d.pop("accessSecret")

        _fluid = d.pop("fluid", UNSET)
        fluid: Union[Unset, ApiFluid]
        if isinstance(_fluid, Unset):
            fluid = UNSET
        else:
            fluid = ApiFluid.from_dict(_fluid)

        new_fluid_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            fluid=fluid,
        )

        return new_fluid_input
