import aiohttp
from typing import Any, Dict

from equia.models import CloudPointCalculationInput, CloudPointCalculationResult, \
    FlashCalculationInput, FlashCalculationResult, \
    FlashedPropertyCalculationInput, FlashedPropertyCalculationResult, \
    PhasediagramFixedTemperaturePressureCalculationInput, PhasediagramFixedTemperaturePressureCalculationResult, \
    FluidAddInput, FluidAddResult, FluidGetInput, FluidGetResult, \
    SlePointCalculationInput, SlePointCalculationResult, \
    UnflashedPropertyCalculationInput, UnflashedPropertyCalculationResult, \
    ProblemDetails \



class EquiaClient:
    """Class for making the calling to Equia API easy"""

    def __init__(self, base_url, user_id, access_secret):
        self.__base_url = "{}/api/01/".format(base_url)
        self.__user_id = user_id
        self.__access_secret = access_secret
        self.__session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False))

    async def cleanup(self):
        """Close session"""
        await self.__session.close()

    def __append_body(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Method that appends user_id and access_secret to the body of the request"""
        user = {
            "userId": self.__user_id,
            "accessSecret": self.__access_secret,
        }
        return {**body, **user}

    async def __post_async(self, endpoint: str, json_body: Dict[str, Any], from_dict):
        """Prepare the URL and the body and makes the POST request to the API"""
        url = "{}{endpoint}".format(self.__base_url, endpoint=endpoint)
        json_body = self.__append_body(json_body)
        try:
            async with self.__session.post(url, json=json_body) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return from_dict(response)
                else:
                    return ProblemDetails.from_dict(response)
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ProblemDetails.from_dict(e)

    async def call_fluid_get_async(
        self,
        body: FluidGetInput,
    ): 
      """Return fluid with givne id"""  
      return await self.__post_async("Fluid/GetFluid", body.to_dict(), FluidGetResult.from_dict)

    async def call_fluid_add_async(
        self,
        body: FluidAddInput,
    ): 
      """Add given fluid to web server and return fluid id"""  
      return await self.__post_async("Fluid/AddFluid", body.to_dict(), FluidAddResult.from_dict)

    async def call_flash_async(
        self,
        body: FlashCalculationInput,
    ):
        """Perform flash calculation"""
        return await self.__post_async("Calculation/Flash", body.to_dict(), FlashCalculationResult.from_dict)

    async def call_cloud_point_async(
        self,
        body: CloudPointCalculationInput,
    ):
        """Perform cloud point calculation"""
        return await self.__post_async("Calculation/CloudPoint", body.to_dict(), CloudPointCalculationResult.from_dict)

    async def call_flashed_properties_async(
        self,
        body: FlashedPropertyCalculationInput,
    ):
        """Perform flash property calculation"""
        return await self.__post_async("Calculation/FlashedProperties", body.to_dict(), FlashedPropertyCalculationResult.from_dict)

    async def call_unflashed_properties_async(
        self,
        body: UnflashedPropertyCalculationInput,
    ):
        """Perform un-flash property calculation"""
        return await self.__post_async("Calculation/UnflashedProperties", body.to_dict(), UnflashedPropertyCalculationResult.from_dict)

    async def call_sle_point_async(
        self,
        body: SlePointCalculationInput,
    ):
        """Perform SLE point calculation"""
        return await self.__post_async("Calculation/SlePoint", body.to_dict(), SlePointCalculationResult.from_dict)

    async def call_phasediagram_standard_async(
        self,
        body: PhasediagramFixedTemperaturePressureCalculationInput,
    ):
        """Perform Phasediagram standard calculation"""
        return await self.__post_async("Calculation/PhasediagramStandard", body.to_dict(), PhasediagramFixedTemperaturePressureCalculationResult.from_dict)

    def get_flash_input(self):
        """Returns flash argument filled with standard input"""
        return FlashCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="", flash_type="Fixed Temperature/Pressure")

    def get_cloud_point_input(self):
        """Returns cloud point argument filled with standard input"""
        return CloudPointCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="", point_type="Fixed Temperature")

    def get_flashed_property_Input(self):
        """Returns flashed properties argument filled with standard input"""
        return FlashedPropertyCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="", property_type="Fixed Temperature/Pressure")

    def get_unflashed_property_input(self):
        """Returns un-flashed properties argument filled with standard input"""
        return UnflashedPropertyCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="", calculation_type="Fixed Temperature/Pressure", volumetype="Auto")

    def get_sle_point_input(self):
        """Returns SLE point argument filled with standard input"""
        return SlePointCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="", point_type="Fixed Pressure")

    def get_phasediagam_standard_input(self):
        """Returns phase diagram standard argument filled with standard input"""
        return PhasediagramFixedTemperaturePressureCalculationInput(user_id=self.__user_id, access_secret=self.__access_secret, units=self.__get_units(), components=[], fluid_id="")

    def get_fluid_get_input(self):
        """Returns request fluid argument filled with standard input"""
        return FluidGetInput(user_id=self.__user_id, access_secret=self.__access_secret)

    def get_fluid_add_input(self):
        """Returns new fluid argument filled with standard input"""
        return FluidAddInput(user_id=self.__user_id, access_secret=self.__access_secret)

    def __get_units(self):
        return "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"
