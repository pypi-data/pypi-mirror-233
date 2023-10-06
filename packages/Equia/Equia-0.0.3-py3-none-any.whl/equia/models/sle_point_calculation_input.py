from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.api_fluid import ApiFluid
from ..types import UNSET, Unset

T = TypeVar("T", bound="SlePointCalculationInput")


@attr.s(auto_attribs=True)
class SlePointCalculationInput:
    """Input for SLE point calculation"""

    user_id: str
    access_secret: str
    components: List[CalculationComposition]
    point_type: str
    units: str
    fluid_id: Union[Unset, str] = UNSET
    fluid: Union[Unset, ApiFluid] = UNSET
    temperature: Union[Unset, float] = UNSET
    pressure: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        access_secret = self.access_secret
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()

            components.append(components_item)

        point_type = self.point_type

        units = self.units

        temperature = self.temperature
        pressure = self.pressure

        fluid_id: Union[Unset, str] = UNSET
        if not isinstance(self.fluid_id, Unset):
            fluid = self.fluid_id

        fluid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fluid, Unset):
            fluid = self.fluid.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "userId": user_id,
                "accessSecret": access_secret,
                "components": components,
                "pointType": point_type,
            }
        )
        if units is not UNSET:
            field_dict["units"] = units
        if fluid_id is not UNSET:
            field_dict["fluidId"] = fluid_id
        if fluid is not UNSET:
            field_dict["fluid"] = fluid
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userId")

        access_secret = d.pop("accessSecret")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(components_item_data)

            components.append(components_item)

        _fluid_id = d.pop("fluidId", UNSET)
        fluid_id: Union[Unset, str]
        if isinstance(_fluid_id, Unset):
            fluid_id = UNSET
        else:
            fluid_id = _fluid_id

        _fluid = d.pop("fluid", UNSET)
        fluid: Union[Unset, ApiFluid]
        if isinstance(_fluid, Unset):
            fluid = UNSET
        else:
            fluid = ApiFluid.from_dict(_fluid)
        point_type = d.pop("pointType")

        units = d.pop("units", UNSET)

        temperature = d.pop("temperature", UNSET)

        pressure = d.pop("pressure", UNSET)

        sle_point_calculation_input = cls(
            user_id=user_id,
            access_secret=access_secret,
            components=components,
            fluid_id=fluid_id,
            fluid=fluid,
            point_type=point_type,
            units=units,
            temperature=temperature,
            pressure=pressure,
        )

        return sle_point_calculation_input
