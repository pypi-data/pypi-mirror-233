from __future__ import annotations
from typeguard import typechecked
from enum import Enum

MAX_ENV_INSTANCE = 3

@typechecked
class Tenant(str, Enum):
    AME = "ame"
    MSFT = "msft"


@typechecked
class Environment(str, Enum):
    TEST = "test"
    DEV = "dev"
    PPE = "ppe"
    PROD = "prod"


@typechecked
class Region(str, Enum):
    ASIA = "asia"
    ASIAPACIFIC = "asiapacific"
    AUSTRALIA = "australia"
    AUSTRALIACENTRAL = "australiacentral"
    AUSTRALIACENTRAL2 = "australiacentral2"
    AUSTRALIAEAST = "australiaeast"
    AUSTRALIASOUTHEAST = "australiasoutheast"
    BRAZIL = "brazil"
    BRAZILSOUTH = "brazilsouth"
    BRAZILSOUTHEAST = "brazilsoutheast"
    CANADA = "canada"
    CANADACENTRAL = "canadacentral"
    CANADAEAST = "canadaeast"
    CENTRALINDIA = "centralindia"
    CENTRALUS = "centralus"
    EASTASIA = "eastasia"
    EASTUS = "eastus"
    EASTUS2 = "eastus2"
    EASTUS2EUAP = "eastus2euap"
    EUROPE = "europe"
    FRANCE = "france"
    FRANCECENTRAL = "francecentral"
    FRANCESOUTH = "francesouth"
    GERMANY = "germany"
    GERMANYNORTH = "germanynorth"
    GERMANYWESTCENTRAL = "germanywestcentral"
    INDIA = "india"
    JAPAN = "japan"
    JAPANEAST = "japaneast"
    JAPANWEST = "japanwest"
    JIOINDIACENTRAL = "jioindiacentral"
    JIOINDIAWEST = "jioindiawest"
    KOREA = "korea"
    KOREACENTRAL = "koreacentral"
    KOREASOUTH = "koreasouth"
    NORTHCENTRALUS = "northcentralus"
    NORTHEUROPE = "northeurope"
    NORWAY = "norway"
    NORWAYEAST = "norwayeast"
    NORWAYWEST = "norwaywest"
    POLANDCENTRAL = "polandcentral"
    SINGAPORE = "singapore"
    SOUTHAFRICA = "southafrica"
    SOUTHAFRICANORTH = "southafricanorth"
    SOUTHAFRICAWEST = "southafricawest"
    SOUTHCENTRALUS = "southcentralus"
    SOUTHEASTASIA = "southeastasia"
    SOUTHINDIA = "southindia"
    SWEDENCENTRAL = "swedencentral"
    SWITZERLAND = "switzerland"
    SWITZERLANDNORTH = "switzerlandnorth"
    SWITZERLANDWEST = "switzerlandwest"
    UAE = "uae"
    UAECENTRAL = "uaecentral"
    UAENORTH = "uaenorth"
    UK = "uk"
    UKSOUTH = "uksouth"
    UKWEST = "ukwest"
    UNITEDSTATES = "unitedstates"
    WESTCENTRALUS = "westcentralus"
    WESTEUROPE = "westeurope"
    WESTINDIA = "westindia"
    WESTUS = "westus"
    WESTUS2 = "westus2"
    WESTUS3 = "westus3"


@typechecked
class Protocol(str, Enum):
    HTTP = "http"
    GRPC = "grpc"

    def __lt__(self, other: Protocol):
        assert isinstance(
            other, Protocol
        ), f"Can only compare Protocol with Protocol, not '{type(other)}'"
        protocols = list(Protocol)
        return protocols.index(self) < protocols.index(other)

    def get_from_value(value: str) -> Protocol:
        if value.lower() in ["http"]:
            return Protocol.HTTP
        elif value.lower() in ["grpc"]:
            return Protocol.GRPC
        else:
            raise ValueError(f"'Protocol' has no name associated with value '{value}'.")


@typechecked
class Auth(str, Enum):
    AAD = "aad"
    KEY = "key"

    def __lt__(self, other: Auth):
        assert isinstance(
            other, Auth
        ), f"Can only compare Auth with Auth, not '{type(other)}'"
        auths = list(Auth)
        return auths.index(self) < auths.index(other)

    def get_from_value(value: str) -> Auth:
        if value.lower() in ["aad", "aadtoken"]:
            return Auth.AAD
        elif value.lower() in ["key"]:
            return Auth.KEY
        else:
            raise ValueError(f"'Auth' has no name associated with value '{value}'.")


@typechecked
class TrafficType(Enum):
    LIVE = 0
    MIRROR = 1

    def __lt__(self, other: TrafficType):
        assert isinstance(
            other, TrafficType
        ), f"Can only compare TrafficType with TrafficType, not '{type(other)}'"
        return self.value > other.value


@typechecked
class InstanceType(str, Enum):
    STANDARD_DS3_V2 = "Standard_DS3_v2"
    STANDARD_F2S_V2 = "Standard_F2s_v2"
    STANDARD_F4S_V2 = "Standard_F4s_v2"
    STANDARD_F8S_V2 = "Standard_F8s_v2"
    STANDARD_F16S_V2 = "Standard_F16s_v2"
    STANDARD_NC6S_V3 = "Standard_NC6s_v3"
    STANDARD_NC4AS_T4_V3 = "Standard_NC4as_T4_v3"
    STANDARD_ND96AMSR_A100_V4 = "Standard_ND96amsr_A100_v4"  # With IB
    STANDARD_ND96AMS_A100_V4 = "Standard_ND96ams_A100_v4"  # Without IB
    STANDARD_NC24ADS_A100_V4 = "Standard_NC24ads_A100_v4"


@typechecked
class Path(Enum):
    SYNC = 0
    ASYNC = 1


@typechecked
class SourceType(str, Enum):
    USER_REQUEST = "USER_REQUEST"
    MODEL_GENERATED = "MODEL_GENERATED"