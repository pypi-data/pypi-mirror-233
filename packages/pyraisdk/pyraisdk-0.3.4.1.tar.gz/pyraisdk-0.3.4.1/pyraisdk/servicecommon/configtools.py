from __future__ import annotations
from collections import OrderedDict
import copy
import csv
from functools import wraps
from hashlib import sha256
import json
import logging
from marshmallow import (
    EXCLUDE,
    fields,
    post_load,
    pre_load,
    RAISE,
    Schema,
    validate,
    validates,
    validates_schema,
)
import math
from pathlib import PosixPath
from typeguard import typechecked
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

from .helpers import Serializable
from .primitives import *

logging.getLogger().setLevel(logging.INFO)


# PRIMITIVES
@typechecked
class Attribute:
    def __init__(self, name: str, datatype: type, is_pk: bool, is_opt: bool):
        self.name = name
        self.datatype = datatype
        self.is_pk = is_pk
        self.is_opt = is_opt


@typechecked
class Record(Serializable):
    ATTRS = []

    def __init__(self, *args, **kwargs):
        for arg_name in kwargs.keys():
            assert arg_name in [
                attr.name for attr in self.ATTRS
            ], f"Unknown attribute '{arg_name}'."
        for attr in self.ATTRS:
            if not attr.is_opt and (
                attr.name not in kwargs or kwargs[attr.name] is None
            ):
                raise ValueError(
                    f"Required attribute '{attr.name}' not provided or is None."
                )
            assert type(kwargs.get(attr.name)) in [
                attr.datatype,
                type(None),
            ], f"Attribute '{attr.name}' must be of type '{attr.datatype}'."
            setattr(self, attr.name, kwargs.get(attr.name))
        self._validate()

    @property
    def pk(self) -> Tuple:
        return tuple(getattr(self, attr.name) for attr in self.ATTRS if attr.is_pk)

    @classmethod
    def make(cls, *args) -> Record:
        assert len(args) == len(cls.ATTRS), f"Expected {len(cls.ATTRS)} arguments."
        return cls(
            **{cls.ATTRS[iidx].name: args[iidx] for iidx in range(len(cls.ATTRS))}
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.pk == other.pk
        return False

    def __hash__(self) -> int:
        return hash(self.pk)

    def _validate(self):
        return


@typechecked
class Table(Serializable):
    RECORD_TYPE = Record

    def __init__(self, records: List[RECORD_TYPE]):
        self._pk_attr_names = [
            attr.name for attr in self.RECORD_TYPE.ATTRS if attr.is_pk
        ]
        self._opt_pk_attr_names = [
            attr.name for attr in self.RECORD_TYPE.ATTRS if attr.is_pk and attr.is_opt
        ]

        def pk_sort_key(record):
            proc_pk_vals = []
            pks = [attr for attr in self.RECORD_TYPE.ATTRS if attr.is_pk]
            for iidx in range(len(pks)):
                pk_datatype = pks[iidx].datatype
                pk_val = record.pk[iidx]
                if pk_datatype is int:
                    proc_pk_val = pk_val if pk_val is not None else 0
                else:
                    proc_pk_val = str(pk_val) if pk_val is not None else ""
                proc_pk_vals.append(proc_pk_val)
            return proc_pk_vals

        records.sort(key=pk_sort_key)
        self._inner_dict = OrderedDict()
        for record in records:
            assert isinstance(
                record, self.RECORD_TYPE
            ), f"Invalid record type '{type(record)}'."
            assert (
                record.pk not in self._inner_dict
            ), f"Multiple {self.RECORD_TYPE.__name__} records have primary key {record.pk}."
            self._inner_dict[record.pk] = record
        self._validate_records()

    @property
    def records(self) -> List[RECORD_TYPE]:
        return list(self._inner_dict.values())

    def _assert_no_dup_contents(self):
        contents_map = {}
        for record in copy.deepcopy(self.records):
            pk = record.pk
            record_attr_map = record.to_dict()
            for name in self._pk_attr_names:
                record_attr_map.pop(name)
            contents = sha256(json.dumps(record_attr_map).encode("utf8")).hexdigest()
            assert (
                contents not in contents_map
            ), f"{self.RECORD_TYPE.__name__} records with primary keys {contents_map[contents]} and {pk} have one or more of the same non-primary key attribute values."
            contents_map[contents] = pk

    def _validate_records(self):
        return

    def export_to_csv(self, file_path: PosixPath):
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow([attr.name for attr in self.RECORD_TYPE.ATTRS])
            for rec in self.records:
                # TEMP until env vars implemented
                writer.writerow(
                    [
                        getattr(rec, attr.name).name
                        if isinstance(
                            getattr(rec, attr.name), (TrafficType, Protocol, Auth)
                        )
                        else getattr(rec, attr.name)
                        for attr in self.RECORD_TYPE.ATTRS
                        if not isinstance(getattr(rec, attr.name), MirrorTrafficTarget)
                    ]
                )

    def filter_by_pks(self, throw_on_empty: bool = False, *args, **kwargs) -> Table:
        for key in kwargs.keys():
            assert key in self._pk_attr_names, f"Invalid primary key attribute '{key}'."
        filtered_records = []
        for record in self.records:
            is_filtered = True
            for key, value in kwargs.items():
                if getattr(record, key) != value:
                    is_filtered = False
            if is_filtered:
                filtered_records.append(record)
        if throw_on_empty:
            assert (
                filtered_records != []
            ), f"No matching {self.RECORD_TYPE.__name__} records when filtering with primary key(s) {kwargs}."
        return type(self)(filtered_records)

    def get_record(
        self, *args, case_insensitive: bool = False, **kwargs
    ) -> RECORD_TYPE:
        if case_insensitive:
            # Assume str pks are case-insensitive.
            for cpk, row in self._inner_dict.items():
                if tuple(pk if type(pk) != str else pk.lower() for pk in cpk) == tuple(
                    pk if type(pk) != str else pk.lower() for pk in args
                ):
                    return row
        else:
            return self._inner_dict[args]
        raise RuntimeError(
            f"Unable to find {self.RECORD_TYPE.__name__} record with primary key {args}."
        )


# COMMON.
# If input data fails validation when attempting to "load" it into a Python
# class, Marshmallow will propagate the data to the "validates" method (if it
# exists) as a dictionary rather than throwing a validation error. As a result,
# the "validates" method is called with invalid data and throws an unhelpful
# error. The "IntSchema" class and "validate_elements" function provide a
# workaround to generate a validation error message.
class IntSchema(Schema):
    def __init__(self, *args, skip_pre_load=False, **kwargs):
        super().__init__(*args, **kwargs)
        if skip_pre_load and hasattr(self, "pre_load"):
            # Skip pre_load method since it may not be idempotent.
            def null_pre_load(data, **kwargs) -> Dict[str, Any]:
                return data

            null_pre_load.__setattr__(
                "__marshmallow_hook__", self.pre_load.__marshmallow_hook__
            )
            self.pre_load = null_pre_load


def validate_elements(schema_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, elements):
            for elem in elements:
                if type(elem) is dict:
                    schema_type(skip_pre_load=True, unknown=RAISE).load(elem)
            return func(self, elements)

        return wrapper

    return decorator


@typechecked
class CommonSchemas:
    Environment = fields.Str(
        required=True,
        validate=validate.OneOf([env.value for env in Environment]),
        metadata={"description": "Deployment target environment."},
    )
    Instance = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=MAX_ENV_INSTANCE),
        metadata={"description": "Deployment target instance."},
    )
    OptInstance = fields.Int(validate=validate.Range(min=0, max=MAX_ENV_INSTANCE))
    Region = fields.Str(
        required=True,
        validate=validate.OneOf([region.value for region in Region]),
        metadata={"description": "Deployment target region."},
    )
    Name = fields.Str(required=True, validate=validate.Length(min=1))
    OptString = fields.Str(validate=validate.Length(min=1))
    Protocol = fields.Str(
        validate=validate.OneOf([p.name for p in Protocol]),
        metadata={"description": "Endpoint protocol."},
    )
    Auth = fields.Str(
        validate=validate.OneOf([a.name for a in Auth]),
        metadata={"description": "Deployment authentication mode."},
    )
    TrafficType = fields.Str(
        validate=validate.OneOf([tt.name for tt in TrafficType]),
        metadata={"description": "Deployment traffic type."},
    )
    InstanceType = fields.Str(
        required=True,
        validate=validate.OneOf([it.value for it in InstanceType]),
        metadata={"description": "VM type to deploy."},
    )
    Version = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        metadata={"description": "Model Version."},
    )
    FileName = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^([^.]+|.+(\.(bin|data|dll|json|model|onnx|opt|pt|pth|py|pyc|tsv|txt|yaml|yml)))$"
        ),
    )
    Container = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^[a-z0-9]([a-z0-9]|(?<=[a-z0-9])-(?=[a-z0-9])){2,62}$"
        ),
        metadata={
            "description": "Storage account container that contains blob artifact(s)."
        },
    )
    DirPath = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        metadata={
            "description": "Path of directory that contains blob artifact(s) relative to parent storage account container."
        },
    )
    RPSPerInstance = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, min_inclusive=False),
        metadata={
            "description": "Number of requests per second that a single model deployment instance can support."
        },
    )

    NonEmptyString = fields.Str(required=True, validate=validate.Length(min=1))
    Path = fields.Str(validate=validate.OneOf([p.name for p in Path]))

    def no_duplicate_files(files: List[File]):
        file_names = set()
        file_hashes = set()
        for file in files:
            file_name = file.Name
            assert file_name not in file_names, f"Multiple files named '{file_name}'."
            file_names.add(file_name)

            file_hash = file.SHA256Hash
            assert (
                file_hash not in file_hashes
                or file_hash
                == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # hash of an empty file
            ), f"Multiple files have hash '{file_hash}'."
            file_hashes.add(file_hash)


# ALLOWLIST.
@typechecked
class AzIdentity(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("Description", str, False, False),
        Attribute("IsCmp", bool, False, False),
    ]


class AzIdentitySchema(IntSchema):
    ObjectId = fields.UUID(required=True)
    Description = CommonSchemas.Name
    IsCmp = fields.Boolean()

    @post_load
    def make(self, data, **kwargs):
        return AzIdentity(**data)


@typechecked
class AzAllowlist(Table):
    RECORD_TYPE = AzIdentity

    @staticmethod
    def make(file_path: PosixPath) -> AzAllowlist:
        with open(file_path, "r") as f:
            return AzAllowlist(
                AzIdentitySchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )


# MATERIALIZED VIEW.
@typechecked
class MaterializedView(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("SourceTable", str, False, False),
        Attribute("Query", str, False, False),
    ]


class MaterializedViewSchema(IntSchema):
    Name = fields.Str(required=True, validate=validate.Length(min=1))
    SourceTable = fields.Str(required=True, validate=validate.Length(min=1))
    Query = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make(self, data, **kwargs):
        return MaterializedView(**data)


@typechecked
class MaterializedViewTable(Table):
    RECORD_TYPE = MaterializedView

    def _validate_records(self):
        self._assert_no_dup_contents()

    @staticmethod
    def make(file_path: PosixPath) -> MaterializedViewTable:
        with open(file_path, "r") as f:
            return MaterializedViewTable(
                MaterializedViewSchema(many=True, unknown=RAISE).load(json.load(f))
            )


# VM QUOTA
@typechecked
class VMFamilyUsageInfo:
    def __init__(self, allocated_count: int, name: str, arm_type: str):
        self.allocated_count = allocated_count
        self.name = name
        self.arm_type = arm_type


class VMFamilyUsageInfoSchema(IntSchema):
    allocated_count = fields.Int(required=True, validate=validate.Range(min=-1))
    name = CommonSchemas.NonEmptyString
    arm_type = CommonSchemas.NonEmptyString

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        data["allocated_count"] = data["limit"]
        data["arm_type"] = data["type"]
        data["name"] = data["name"]["value"]
        return data

    @post_load
    def make(self, data, **kwargs):
        return VMFamilyUsageInfo(**data)


@typechecked
class VMFamilyUsageInfoSet:
    def __init__(self, inner_set: List[VMFamilyUsageInfo]):
        self._inner_set = set(inner_set)

    @staticmethod
    def make_from_dict(input_dict: Dict[str, Any]) -> VMFamilyUsageInfoSet:
        return VMFamilyUsageInfoSet(
            VMFamilyUsageInfoSchema(many=True, unknown=EXCLUDE).load(
                input_dict["value"]
            )
        )

    def get_vm_family_usage_info(self, family: str) -> VMFamilyUsageInfo:
        for vm_family_usage_info in self._inner_set:
            if (
                "dedicatedCores" in vm_family_usage_info.arm_type
                and vm_family_usage_info.name == family
            ):
                return vm_family_usage_info
        raise RuntimeError(
            f"Unable to find usage information for VM family '{family}'."
        )


# TODO: Validate InstanceTypes with VMSizeInfoSet.
@typechecked
class VMSizeInfo:
    def __init__(self, family_name: str, name: str, core_count: int):
        self.family_name = family_name
        self.name = name
        self.core_count = core_count


class VMSizeInfoSchema(IntSchema):
    family_name = CommonSchemas.NonEmptyString
    name = CommonSchemas.NonEmptyString
    core_count = fields.Int(required=True, validate=validate.Range(min=1))

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        data["family_name"] = data["family"]
        data["core_count"] = data["vCPUs"]
        return data

    @post_load
    def make(self, data, **kwargs):
        return VMSizeInfo(**data)


@typechecked
class VMSizeInfoSet:
    def __init__(self, inner_set: List[VMSizeInfo]):
        self._inner_set = set(inner_set)

    @staticmethod
    def make_from_dict(input_dict: Dict[str, Any]) -> VMSizeInfoSet:
        return VMSizeInfoSet(
            VMSizeInfoSchema(many=True, unknown=EXCLUDE).load(input_dict["value"])
        )

    def get_vm_size_info(self, name: str) -> VMSizeInfo:
        for vm_size in self._inner_set:
            if vm_size.name == name:
                return vm_size
        raise RuntimeError(f"Unable to find size information for VM '{name}'.")


# OPENAI Model
@typechecked
class OpenAIModel(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("Description", str, False, False),
    ]


class OpenAIModelSchema(Schema):
    Name = CommonSchemas.Name
    Description = CommonSchemas.OptString

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        return data

    @post_load
    def make(self, data, **kwargs):
        return OpenAIModel(**data)


@typechecked
class OpenAIModelTable(Table):
    RECORD_TYPE = OpenAIModel

    @staticmethod
    def make(file_path: PosixPath) -> OpenAIModelTable:
        with open(file_path, "r") as f:
            return OpenAIModelTable(
                OpenAIModelSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )


# CUSTOMER GPU CONFIGURATION
@typechecked
class CustomerGPUConfig(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("ObjectCoarseId", str, True, True),
        Attribute("OpenAIModel", str, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("InstanceCount", int, False, False),
    ]


class CustomerGPUConfigSchema(IntSchema):
    ObjectId = fields.UUID(required=True)
    ObjectCoarseId = CommonSchemas.OptString
    OpenAIModel = CommonSchemas.Name
    InstanceType = CommonSchemas.InstanceType
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    InstanceCount = fields.Int(required=True, validate=validate.Range(min=1))

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["ObjectCoarseId"] == "":
            data.pop("ObjectCoarseId")
        return data

    @post_load
    def make(self, data, **kwargs):
        data["InstanceType"] = InstanceType(data["InstanceType"])
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        return CustomerGPUConfig(**data)


@typechecked
class CustomerGPUConfigTable(Table):
    RECORD_TYPE = CustomerGPUConfig

    @staticmethod
    def make(
        file_path: PosixPath,
        customer_table: CustomerTable,
        openai_model_table: OpenAIModelTable,
        cluster_table: ClusterTable,
    ) -> CustomerGPUConfigTable:
        with open(file_path, "r") as f:
            customer_gpu_config_table = CustomerGPUConfigTable(
                CustomerGPUConfigSchema(many=True, unknown=RAISE).load(
                    csv.DictReader(f)
                )
            )
        customer_gpu_config_table.validate_in_ctx(
            customer_table, openai_model_table, cluster_table
        )
        return customer_gpu_config_table

    def validate_in_ctx(
        self,
        customer_table: CustomerTable,
        openai_model_table: OpenAIModelTable,
        cluster_table: ClusterTable,
    ):
        for customer_gpu_config in self.records:
            customer_table.get_record(
                customer_gpu_config.ObjectId, customer_gpu_config.ObjectCoarseId
            )
            openai_model_table.get_record(customer_gpu_config.OpenAIModel)
            cluster_table.get_record(
                customer_gpu_config.Environment,
                customer_gpu_config.Instance,
                customer_gpu_config.Region,
            )


# OPENAI MODEL PERFORMANCE
@typechecked
class OpenAIModelPerf(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("ObjectCoarseId", str, True, True),
        Attribute("OpenAIModel", str, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("RPSPerInstance", float, False, False),
    ]


class OpenAIModelPerfSchema(Schema):
    ObjectId = fields.UUID(required=True)
    ObjectCoarseId = CommonSchemas.OptString
    OpenAIModel = CommonSchemas.Name
    InstanceType = CommonSchemas.InstanceType
    RPSPerInstance = CommonSchemas.RPSPerInstance

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["ObjectCoarseId"] == "":
            data.pop("ObjectCoarseId")
        return data

    @post_load
    def make(self, data, **kwargs):
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return OpenAIModelPerf(**data)


@typechecked
class OpenAIModelPerfTable(Table):
    RECORD_TYPE = OpenAIModelPerf

    @staticmethod
    def make(
        file_path: PosixPath,
        customer_table: CustomerTable,
        openai_model_table: OpenAIModelTable,
    ) -> OpenAIModelPerfTable:
        with open(file_path, "r") as f:
            openai_model_perf_table = OpenAIModelPerfTable(
                OpenAIModelPerfSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )
        openai_model_perf_table.validate_in_ctx(customer_table, openai_model_table)
        return openai_model_perf_table

    def validate_in_ctx(
        self, customer_table: CustomerTable, openai_model_table: OpenAIModelTable
    ):
        for openai_model_perf in self.records:
            customer_table.get_record(
                openai_model_perf.ObjectId, openai_model_perf.ObjectCoarseId
            )
            openai_model_table.get_record(openai_model_perf.OpenAIModel)


# MODEL ENDPOINT AND IN-PROCESS MODEL LOAD PARAMETERS
@typechecked
class ModelLoadParams(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("ObjectCoarseId", str, True, True),
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute(
            "Protocol", Protocol, False, False
        ),  # In-process models are keyed by name only.
        Attribute("Path", Path, True, False),
        Attribute("SourceType", SourceType, True, False),
        Attribute("FanOut", float, False, False),
    ]


class ModelEndpointLoadParamsSchema(Schema):
    ObjectId = fields.UUID(required=True)
    ObjectCoarseId = CommonSchemas.OptString
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Path = fields.Str(required=True, validate=validate.OneOf([p.name for p in Path]))
    SourceType = fields.Str(
        required=True,
        validate=validate.OneOf([env.value for env in SourceType]),
        metadata={
            "description": "Specifies whether a request originated from a user or OpenAI model."
        },
    )
    FanOut = fields.Float(
        required=True, validate=validate.Range(min=0.0, min_inclusive=False)
    )

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["ObjectCoarseId"] == "":
            data.pop("ObjectCoarseId")
        return data

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        data["Path"] = Path[data["Path"]]
        data["SourceType"] = SourceType[data["SourceType"]]
        if "Protocol" in data:
            data["Protocol"] = Protocol[data["Protocol"]]
        return ModelLoadParams(**data)


@typechecked
class ModelEndpointLoadParamsTable(Table):
    RECORD_TYPE = ModelLoadParams

    @staticmethod
    def make(
        file_path: PosixPath,
        customer_table: CustomerTable,
        cluster_table: ClusterTable,
        model_ep_table: ModelEndpointTable,
    ) -> ModelEndpointLoadParamsTable:
        with open(file_path, "r") as f:
            model_endpoint_load_params_table = ModelEndpointLoadParamsTable(
                ModelEndpointLoadParamsSchema(many=True, unknown=RAISE).load(
                    csv.DictReader(f)
                )
            )
            model_endpoint_load_params_table.validate_in_ctx(
                customer_table, cluster_table, model_ep_table
            )
            return model_endpoint_load_params_table

    def validate_in_ctx(
        self,
        customer_table: CustomerTable,
        cluster_table: ClusterTable,
        model_ep_table: ModelEndpointTable,
    ):
        for model_endpoint_load_params in self.records:
            customer_table.get_record(
                model_endpoint_load_params.ObjectId,
                model_endpoint_load_params.ObjectCoarseId,
            )
            cluster_table.get_record(
                model_endpoint_load_params.Environment,
                model_endpoint_load_params.Instance,
                model_endpoint_load_params.Region,
            )
            # TODO: validate in-process model names
            if model_endpoint_load_params.Protocol is not None:
                model_ep_table.get_record(
                    model_endpoint_load_params.Name,
                    model_endpoint_load_params.Protocol,
                )


# CUSTOMER.
@typechecked
class Customer(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("ObjectCoarseId", str, True, True),
        Attribute("Description", str, False, False),
    ]


class CustomerSchema(IntSchema):
    ObjectId = fields.UUID(required=True)
    ObjectCoarseId = CommonSchemas.OptString
    Description = CommonSchemas.Name

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["ObjectCoarseId"] == "":
            data.pop("ObjectCoarseId")
        return data

    @post_load
    def make(self, data, **kwargs):
        return Customer(**data)


@typechecked
class CustomerTable(Table):
    RECORD_TYPE = Customer

    @staticmethod
    def make(file_path: PosixPath, allowlist: AzAllowlist) -> CustomerTable:
        with open(file_path, "r") as f:
            customer_table = CustomerTable(
                CustomerSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )
        customer_table.validate_in_ctx(allowlist)
        return customer_table

    def validate_in_ctx(self, allowlist: AzAllowlist):
        for rec in self.records:
            allowlist.get_record(rec.ObjectId)


# ENGINEER.
@typechecked
class Engineer(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("MicrosoftAlias", str, False, False),
        Attribute("GitHubAlias", str, False, False),
        Attribute("TeamName", str, False, False),
    ]


class EngineerSchema(IntSchema):
    Name = CommonSchemas.Name
    MicrosoftAlias = CommonSchemas.Name
    GitHubAlias = CommonSchemas.Name
    TeamName = CommonSchemas.Name

    @post_load
    def make(self, data, **kwargs):
        return Engineer(**data)


@typechecked
class EngineerTable(Table):
    RECORD_TYPE = Engineer

    @staticmethod
    def make(file_path: PosixPath) -> EngineerTable:
        with open(file_path, "r") as f:
            return EngineerTable(
                EngineerSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )


@typechecked
class EngineerTeam(Record):
    ATTRS = [
        Attribute("TeamName", str, True, False),
        Attribute("IcmTeamName", str, False, False),
        Attribute("GitHubOrg", str, False, False),
        Attribute("GitHubRepo", str, False, False),
    ]


class EngineerTeamSchema(IntSchema):
    TeamName = CommonSchemas.Name
    IcmTeamName = CommonSchemas.Name
    GitHubOrg = CommonSchemas.Name
    GitHubRepo = CommonSchemas.Name

    @post_load
    def make(self, data, **kwargs):
        return EngineerTeam(**data)


@typechecked
class EngineerTeamTable(Table):
    RECORD_TYPE = EngineerTeam

    @staticmethod
    def make(file_path: PosixPath) -> EngineerTeamTable:
        with open(file_path, "r") as f:
            return EngineerTeamTable(
                EngineerTeamSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )

    def validate_in_ctx(self, engineer_table: EngineerTable):
        for engineer in engineer_table.records:
            self.get_record(engineer.TeamName)


class IcmTeam(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("Id", int, False, False),
        Attribute("PublicId", str, False, False),
    ]


class IcmTeamSchema(IntSchema):
    Name = CommonSchemas.Name
    Id = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        metadata={"description": "Identification Code"},
    )
    PublicId = CommonSchemas.Name

    @post_load
    def make(self, data, **kwargs):
        return IcmTeam(**data)


@typechecked
class IcmTeamTable(Table):
    RECORD_TYPE = IcmTeam

    @staticmethod
    def make(file_path: PosixPath) -> IcmTeamTable:
        with open(file_path, "r") as f:
            return IcmTeamTable(
                IcmTeamSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )

    def validate_in_ctx(self, engineer_team_table: EngineerTeamTable):
        for engineer_team in engineer_team_table.records:
            self.get_record(engineer_team.IcmTeamName)


# MODEL ENDPOINT CONFIGURATION.
@typechecked
class AuthConfig(Serializable):
    def __init__(self, Username: str, PasswordKeyVaultSecretName: str):
        self.Username = Username
        self.PasswordKeyVaultSecretName = PasswordKeyVaultSecretName


class AuthConfigSchema(IntSchema):
    Username = fields.Str(required=True, validate=validate.Length(min=1))
    PasswordKeyVaultSecretName = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[-a-zA-Z0-9]{1,127}$"),
        metadata={
            "description": "Name of secret in RAI global key vault that contains container registry password."
        },
    )

    @post_load
    def make(self, data, **kwargs):
        return AuthConfig(**data)


@typechecked
class DockerConfig(Serializable):
    def __init__(self, Domain: str, Registry: str, AuthConfig: AuthConfig = None):
        self.Domain = Domain
        self.Registry = Registry
        self.AuthConfig = AuthConfig


class DockerConfigSchema(IntSchema):
    Domain = fields.Str(required=True, validate=validate.Regexp(r".+\.(com|io)$"))
    Registry = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Name of Docker image registry."},
    )
    AuthConfig = fields.Nested(AuthConfigSchema, unknown=RAISE)

    @post_load
    def make(self, data, **kwargs):
        return DockerConfig(**data)


@typechecked
class StorageAccountConfig(Serializable):
    def __init__(self, Name: str, SasTokenKeyVaultSecretName: str):
        self.Name = Name
        self.SasTokenKeyVaultSecretName = SasTokenKeyVaultSecretName


class StorageAccountConfigSchema(IntSchema):
    Name = fields.Str(required=True, validate=validate.Regexp(r"^[a-z0-9]{3,24}$"))
    SasTokenKeyVaultSecretName = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[-a-zA-Z0-9]{1,127}$"),
        metadata={
            "description": "Name of secret in RAI global key vault that contains storage account SAS token."
        },
    )

    @post_load
    def make(self, data, **kwargs):
        return StorageAccountConfig(**data)


@typechecked
class RemoteConfig(Serializable):
    def __init__(
        self,
        DockerConfig: DockerConfig,
        StorageAccountConfig: StorageAccountConfig = None,
    ):
        self.DockerConfig = DockerConfig
        self.StorageAccountConfig = StorageAccountConfig


class RemoteConfigSchema(IntSchema):
    DockerConfig = fields.Nested(
        DockerConfigSchema,
        required=True,
        unknown=RAISE,
        metadata={
            "description": "Docker container registry that contains image used to deploy AML environment."
        },
    )
    StorageAccountConfig = fields.Nested(
        StorageAccountConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Storage account that contains blobs used to deploy AML resources."
        },
    )

    @post_load
    def make(self, data, **kwargs):
        return RemoteConfig(**data)


@typechecked
class Route(Serializable):
    def __init__(self, Path: str, Port: int):
        self.Path = Path
        self.Port = Port

    def validate_config_changes(self, prev: Route):
        assert (
            self.Path == prev.Path
        ), f"Current and previous 'Path' values must be equal."
        assert (
            self.Port == prev.Port
        ), f"Current and previous 'Port' values must be equal."


class RouteSchema(IntSchema):
    Path = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\/.*"),
        metadata={"description": "Endpoint request path."},
    )
    Port = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        metadata={"description": "Endpoint request port."},
    )

    @post_load
    def make(self, data, **kwargs):
        return Route(**data)


@typechecked
class InferenceConfig(Serializable):
    def __init__(
        self, LivenessRoute: Route, ReadinessRoute: Route, ScoringRoute: Route
    ):
        self.LivenessRoute = LivenessRoute
        self.ReadinessRoute = ReadinessRoute
        self.ScoringRoute = ScoringRoute

    def validate_config_changes(self, prev: InferenceConfig):
        try:
            self.LivenessRoute.validate_config_changes(prev.LivenessRoute)
        except Exception as ex:
            raise AssertionError(
                f"Error while validating changes to 'LivenessRoute'. Error: {ex}"
            )
        try:
            self.ReadinessRoute.validate_config_changes(prev.ReadinessRoute)
        except Exception as ex:
            raise AssertionError(
                f"Error while validating changes to 'ReadinessRoute'. Error: {ex}"
            )
        try:
            self.ScoringRoute.validate_config_changes(prev.ScoringRoute)
        except Exception as ex:
            raise AssertionError(
                f"Error while validating changes to 'ScoringRoute'. Error: {ex}"
            )


class InferenceConfigSchema(IntSchema):
    LivenessRoute = fields.Nested(
        RouteSchema,
        required=True,
        unknown=RAISE,
        metadata={
            "description": "Route to check the liveness of the inference server container."
        },
    )
    ReadinessRoute = fields.Nested(
        RouteSchema,
        required=True,
        unknown=RAISE,
        metadata={
            "description": "Route to check the readiness of the inference server container."
        },
    )
    ScoringRoute = fields.Nested(
        RouteSchema,
        required=True,
        unknown=RAISE,
        metadata={
            "description": "Route to send scoring requests to within the inference server container."
        },
    )

    @post_load
    def make(self, data, **kwargs):
        return InferenceConfig(**data)


@typechecked
class ModelEndpoint(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("Description", str, False, False),
        Attribute("Owner", str, False, False),
        Attribute("OwningTeam", str, False, False),
        Attribute("SamplePostData", str, False, True),
        Attribute("NonAMLUrl", str, False, True),
        Attribute("RemoteConfig", RemoteConfig, False, True),
        Attribute("InferenceConfig", InferenceConfig, False, True),
    ]

    def validate_config_changes(self, prev: ModelEndpoint):
        assert (
            self.Name == prev.Name
        ), f"Current and previous model names '{self.Name}' and '{prev.Name}' do not match."
        assert (
            self.Protocol == prev.Protocol
        ), f"Current and previous Protocol values must be equal."
        assert (
            self.NonAMLUrl == prev.NonAMLUrl
        ), f"Current and previous NonAMLUrl values must be equal."
        assert (
            self.SamplePostData == prev.SamplePostData
        ), f"Current and previous SamplePostData values must be equal."
        if self.InferenceConfig is None:
            assert (
                prev.InferenceConfig is None
            ), f"'InferenceConfig' deleted from configuration."
        else:
            assert (
                prev.InferenceConfig is not None
            ), f"'InferenceConfig' added to configuration."
            try:
                self.InferenceConfig.validate_config_changes(prev.InferenceConfig)
            except Exception as ex:
                raise AssertionError(
                    f"Error while validating changes to InferenceConfig. Error: {ex}"
                )


class ModelEndpointSchema(IntSchema):
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Description = CommonSchemas.Name
    Owner = CommonSchemas.Name
    OwningTeam = CommonSchemas.Name
    SamplePostData = fields.Raw(
        metadata={
            "description": 'Sample data passed to curl command when verifying endpoint functionality. Example: {"data": ["Hello, World."]}.'
        }
    )
    NonAMLUrl = fields.Str(
        required=True,
        metadata={
            "description": "Full URL for non-AML endpoint. Leave blank if AML endpoint configured."
        },
    )
    # RemoteConfig should theoretically be an attribute of
    # ModelDeploymentConfig since it is not necessarily constant for a given
    # endpoint, but we're assuming it will always be constant to avoid
    # configuration bloat.
    RemoteConfig = fields.Nested(
        RemoteConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Defines external resources required to locate and access blob and image artifacts used to create AML resources."
        },
    )
    # RemoteConfig should theoretically be an attribute of
    # ModelDeploymentConfig since it is not necessarily constant for a given
    # endpoint, but we're assuming it will always be constant to simplify
    # orchestrator's logic when inferencing against the endpoint.
    InferenceConfig = fields.Nested(
        InferenceConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Inference container configuration optionally used to create AML environment."
        },
    )

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if "Protocol" in data:
            assert (
                Protocol[data["Protocol"]] == Protocol.GRPC
            ), "Only set Protocol if value is GRPC. Protocol is assumed to be HTTP otherwise."
        else:
            data["Protocol"] = Protocol.HTTP.name
        return data

    @validates_schema
    def validates_schema(self, data, **kwargs):
        sample_post_data = data.get("SamplePostData")
        if data["Protocol"] == Protocol.GRPC.name:
            assert (
                sample_post_data is None
            ), "GRPC endpoints must not have SamplePostData."
        else:
            assert (
                sample_post_data is not None
            ), "HTTP endpoints must have SamplePostData."

    @post_load
    def make(self, data, **kwargs):
        data["Protocol"] = Protocol[data["Protocol"]]
        return ModelEndpoint(**data)


@typechecked
class ModelEndpointTable(Table):
    RECORD_TYPE = ModelEndpoint

    # TODO: reenable
    # def _validate_records(self):
    #     assert self.records == sorted(
    #         self.records, key=lambda x: (x.Name.lower(), x.Protocol)
    #     ), "Endpoint configurations must be sorted alphabetically then by Protocol (HTTP before GRPC)."

    @staticmethod
    def make(file_path: PosixPath, engineer_table: EngineerTable) -> ModelEndpointTable:
        with open(file_path, "r") as f:
            model_ep_table = ModelEndpointTable(
                ModelEndpointSchema(many=True, unknown=RAISE).load(json.load(f))
            )
        model_ep_table.validate_in_ctx(engineer_table)
        return model_ep_table

    def validate_in_ctx(self, engineer_table: EngineerTable):
        for model_ep in self.records:
            engineer_table.get_record(model_ep.Owner)


# MODEL DEPLOYMENT CONFIGURATION.
@typechecked
class BatchingConfig(Serializable):
    def __init__(
        self,
        MaxBatchSize: int,
        IdleBatchSize: int,
        MaxBatchInterval: float,
    ):
        self.MaxBatchSize = MaxBatchSize
        self.IdleBatchSize = IdleBatchSize
        self.MaxBatchInterval = MaxBatchInterval


class BatchingConfigSchema(IntSchema):
    MaxBatchSize = fields.Int(required=True, validate=validate.Range(min=1))
    IdleBatchSize = fields.Int(required=True, validate=validate.Range(min=1))
    MaxBatchInterval = fields.Float(
        required=True, validate=validate.Range(min=0.0, min_inclusive=False)
    )

    @validates_schema
    def validates_schema(self, data, **kwargs):
        max_size = data["MaxBatchSize"]
        idle_size = data["IdleBatchSize"]
        assert (
            max_size >= idle_size
        ), f"MaxBatchSize ({max_size}) must be greater than or equal to IdleBatchSize ({idle_size})."

    @post_load
    def make(self, data, **kwargs):
        return BatchingConfig(**data)


@typechecked
class PerfConfig(Serializable):
    def __init__(
        self,
        InstanceType: InstanceType,
        BatchingConfig: BatchingConfig,
    ):
        self.InstanceType = InstanceType
        self.BatchingConfig = BatchingConfig


class PerfConfigSchema(IntSchema):
    InstanceType = CommonSchemas.InstanceType
    BatchingConfig = fields.Nested(
        BatchingConfigSchema,
        required=True,
        unknown=RAISE,
        metadata={"description": "Dynamic batching configuration."},
    )

    @post_load
    def make(self, data, **kwargs):
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return PerfConfig(**data)


@typechecked
class File(Serializable):
    def __init__(self, Name: str, SHA256Hash: str):
        self.Name = Name
        self.SHA256Hash = SHA256Hash

    def __eq__(self, other: File) -> bool:
        return self.Name == other.Name and self.SHA256Hash == other.SHA256Hash

    def __hash__(self) -> int:
        return hash((self.Name, self.SHA256Hash))

    def validate_config_changes(self, prev: File):
        assert (
            self.SHA256Hash == prev.SHA256Hash
        ), f"Current and previous hash values do not match for file '{self.Name}'."


class FileSchema(IntSchema):
    Name = CommonSchemas.FileName
    SHA256Hash = fields.Str(
        required=True,
        validate=validate.Regexp(r"^[a-fA-F0-9]{64}$"),
        metadata={"description": "SHA256 hash of the file."},
    )

    @post_load
    def make(self, data, **kwargs):
        return File(**data)


@typechecked
class StorageAccountArtifactsConfig(Serializable):
    def __init__(self, Container: str, DirPath: str, Files: List[File]):
        self.Container = Container
        self.DirPath = DirPath
        self.Files = set(Files)

    def get_files(self) -> Set[File]:
        return self.Files

    def get_file(self, name: str) -> File:
        for file in self.Files:
            if file.Name == name:
                return file
        raise RuntimeError(f"Unable to find file '{name}'.")

    def validate_config_changes(self, prev: StorageAccountArtifactsConfig):
        assert self.get_files() == prev.get_files(), "File sets must be equal."
        for curr_file in self.get_files():
            try:
                curr_file.validate_config_changes(prev.get_file(curr_file.Name))
            except Exception as ex:
                raise AssertionError(
                    f"Error while validating changes to file '{curr_file.Name}'. Error: {ex}"
                )


@typechecked
class CodeConfig(StorageAccountArtifactsConfig):
    def __init__(
        self, Container: str, DirPath: str, Files: List[File], ScoringScript: str
    ):
        super().__init__(Container, DirPath, Files)
        self.ScoringScript = ScoringScript

    def validate_config_changes(self, prev: CodeConfig):
        StorageAccountArtifactsConfig.validate_config_changes(self, prev)
        assert (
            self.ScoringScript == prev.ScoringScript
        ), f"Current and previous scoring scripts '{self.ScoringScript}' and '{prev.ScoringScript}' do not match."


class CodeConfigSchema(IntSchema):
    Container = CommonSchemas.Container
    DirPath = CommonSchemas.DirPath
    Files = fields.Nested(
        FileSchema,
        required=True,
        many=True,
        unknown=RAISE,
        validate=CommonSchemas.no_duplicate_files,
    )
    ScoringScript = CommonSchemas.FileName

    @validates_schema
    def validates_schema(self, data, **kwargs):
        assert data["ScoringScript"] in [
            file.Name for file in data["Files"]
        ], f"Scoring script '{data['ScoringScript']}' does not match name of one of the CodeConfig files."

    @post_load
    def make(self, data, **kwargs):
        return CodeConfig(**data)


@typechecked
class CondaFileConfig(StorageAccountArtifactsConfig):
    def __init__(self, Container: str, DirPath: str, File: File):
        super().__init__(Container, DirPath, [File])
        self.File = File
        self.__delattr__("Files")

    def get_files(self) -> Set[File]:
        return {self.File}

    def get_file(self, name: str) -> File:
        if self.File.Name == name:
            return self.File
        raise RuntimeError(f"Unable to find file '{name}'.")


class CondaFileConfigSchema(IntSchema):
    Container = CommonSchemas.Container
    DirPath = CommonSchemas.DirPath
    File = fields.Nested(FileSchema, required=True, unknown=RAISE)

    @post_load
    def make(self, data, **kwargs):
        return CondaFileConfig(**data)


@typechecked
class ImageConfig(Serializable):
    def __init__(self, Repository: str, Tag: str):
        self.Repository = Repository
        self.Tag = Tag

    def validate_config_changes(self, prev: ImageConfig):
        assert (
            self.Repository == prev.Repository
        ), f"Current and previous image repositories '{self.Repository}' and '{prev.Repository}' do not match."
        assert (
            self.Tag == prev.Tag
        ), f"Current and previous image tags '{self.Tag}' and '{prev.Tag}' do not match."


class ImageConfigSchema(IntSchema):
    Repository = fields.Str(required=True, validate=validate.Length(min=1))
    Tag = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make(self, data, **kwargs):
        return ImageConfig(**data)


@typechecked
class EnvironmentConfig(Serializable):
    def __init__(
        self,
        ImageConfig: ImageConfig,
        CondaFileConfig: CondaFileConfig = None,
    ):
        self.CondaFileConfig = CondaFileConfig
        self.ImageConfig = ImageConfig

    def validate_config_changes(self, prev: EnvironmentConfig):
        if self.CondaFileConfig is None:
            assert (
                prev.CondaFileConfig is None
            ), f"'CondaFileConfig' deleted from configuration."
        else:
            assert (
                prev.CondaFileConfig is not None
            ), f"'CondaFileConfig' added to configuration."
            try:
                self.CondaFileConfig.validate_config_changes(prev.CondaFileConfig)
            except Exception as ex:
                raise AssertionError(
                    f"Error while validating changes to CondaFileConfig. Error: {ex}"
                )
        try:
            self.ImageConfig.validate_config_changes(prev.ImageConfig)
        except Exception as ex:
            raise AssertionError(
                f"Error while validating changes to ImageConfig. Error: {ex}"
            )


class EnvironmentConfigSchema(IntSchema):
    CondaFileConfig = fields.Nested(
        CondaFileConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Configuration for conda YAML configuration file that lists AML environment dependencies."
        },
    )
    ImageConfig = fields.Nested(
        ImageConfigSchema,
        required=True,
        unknown=RAISE,
        metadata={"description": "AML environment image configuration."},
    )

    @post_load
    def make(self, data, **kwargs):
        return EnvironmentConfig(**data)


@typechecked
class ModelConfig(StorageAccountArtifactsConfig):
    def __init__(self, Container: str, DirPath: str, Files: List[File]):
        super().__init__(Container, DirPath, Files)


class ModelConfigSchema(IntSchema):
    Container = CommonSchemas.Container
    DirPath = CommonSchemas.DirPath
    Files = fields.Nested(
        FileSchema,
        required=True,
        many=True,
        unknown=RAISE,
        validate=CommonSchemas.no_duplicate_files,
    )

    @post_load
    def make(self, data, **kwargs):
        return ModelConfig(**data)


@typechecked
class IntModelDeployment(Serializable):
    def __init__(
        self,
        Version: int,
        Description: str,
        MaxConcurrentRequestsPerInstance: int,
        EnvironmentConfig: EnvironmentConfig,
        TrafficType: TrafficType = TrafficType.LIVE,
        PerfConfigs: List[PerfConfig] = None,
        CodeConfig: CodeConfig = None,
        ModelConfig: ModelConfig = None,
    ):
        self.TrafficType = TrafficType
        self.Version = Version
        self.Description = Description
        self.PerfConfigs = PerfConfigs
        self.CodeConfig = CodeConfig
        self.MaxConcurrentRequestsPerInstance = MaxConcurrentRequestsPerInstance
        self.EnvironmentConfig = EnvironmentConfig
        self.ModelConfig = ModelConfig


class IntModelDeploymentSchema(IntSchema):
    TrafficType = CommonSchemas.TrafficType
    Version = CommonSchemas.Version
    Description = CommonSchemas.Name
    PerfConfigs = fields.Nested(
        PerfConfigSchema,
        many=True,
        unknown=RAISE,
    )
    CodeConfig = fields.Nested(
        CodeConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Configuration for blob artifacts optionally used to create AML code."
        },
    )
    MaxConcurrentRequestsPerInstance = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        metadata={"description": "Maximum number of concurrent requests per instance."},
    )
    EnvironmentConfig = fields.Nested(
        EnvironmentConfigSchema,
        required=True,
        unknown=RAISE,
        metadata={
            "description": "Defines parameters necessary to create AML environment."
        },
    )
    ModelConfig = fields.Nested(
        ModelConfigSchema,
        unknown=RAISE,
        metadata={
            "description": "Configuration for blob artifacts optionally used to create AML model."
        },
    )

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if "TrafficType" in data:
            assert (
                TrafficType[data["TrafficType"]] == TrafficType.MIRROR
            ), "Only set TrafficType for mirror traffic model deployment configurations. TrafficType is assumed to be LIVE otherwise."
        else:
            data["TrafficType"] = TrafficType.LIVE.name
        return data

    @validates("PerfConfigs")
    @validate_elements(PerfConfigSchema)
    def non_empty_perf_configs(self, value: List[PerfConfig]):
        assert len(value) > 0, "Must specify at least one PerfConfig or leave null."

    @post_load
    def make(self, data, **kwargs):
        data["TrafficType"] = TrafficType[data["TrafficType"]]
        return IntModelDeployment(**data)


@typechecked
class IntModelDeployments(Serializable):
    def __init__(
        self,
        Name: str,
        ModelDeployments: List[IntModelDeployment],
        Protocol: Protocol = Protocol.HTTP,
    ):
        self.Name = Name
        self.Protocol = Protocol
        self.inner = set(ModelDeployments)


class IntModelDeploymentsSchema(IntSchema):
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    ModelDeployments = fields.Nested(
        IntModelDeploymentSchema,
        required=True,
        many=True,
        unknown=RAISE,
        metadata={"description": "Parameters necessary to deploy model."},
    )

    @validates("ModelDeployments")
    @validate_elements(IntModelDeploymentSchema)
    def validate_model_deps(self, value: List[ModelDeployments]):
        assert value == sorted(
            value, key=lambda x: (x.TrafficType, x.Version), reverse=True
        ), "Deployment configurations must be grouped by TrafficType (LIVE before MIRROR) and sorted in decreasing order."

    @post_load
    def make(self, data, **kwargs):
        if "Protocol" in data:
            data["Protocol"] = Protocol[data["Protocol"]]
        return IntModelDeployments(**data)


@typechecked
class IntModelDeploymentTable:
    def __init__(self, inner: List[IntModelDeployments]):
        self._inner = set(inner)

    @staticmethod
    def make(dir_path: PosixPath) -> IntModelDeploymentTable:
        all_int_model_deps = []
        for int_model_deps_file in dir_path.iterdir():
            with open(dir_path.joinpath(int_model_deps_file), "r") as f:
                int_model_deps = IntModelDeploymentsSchema(unknown=RAISE).load(
                    json.load(f)
                )
            all_int_model_deps.append(int_model_deps)
        return IntModelDeploymentTable(all_int_model_deps)


@typechecked
class ModelSKUBatchingConfig(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("MaxBatchSize", int, False, False),
        Attribute("IdleBatchSize", int, False, False),
        Attribute("MaxBatchInterval", float, False, False),
    ]

    def validate_config_changes(self, prev: ModelSKUBatchingConfig):
        assert (
            self.MaxBatchSize == prev.MaxBatchSize
        ), f"Current and previous MaxBatchSize values for ModelSKUBatchingConfig with primary key {self.pk} do not match."
        assert (
            self.IdleBatchSize == prev.IdleBatchSize
        ), f"Current and previous IdleBatchSize values for ModelSKUBatchingConfig with primary key {self.pk} do not match."
        assert (
            self.MaxBatchInterval == prev.MaxBatchInterval
        ), f"Current and previous MaxBatchInterval values for ModelSKUBatchingConfig with primary key {self.pk} do not match."


@typechecked
class ModelSKUBatchingConfigTable(Table):
    RECORD_TYPE = ModelSKUBatchingConfig

    @staticmethod
    def make_from_int_model_dep_table(
        int_model_dep_table: IntModelDeploymentTable,
    ) -> ModelSKUBatchingConfigTable:
        model_sku_batching_configs = []
        for int_model_deps in int_model_dep_table._inner:
            for int_model_dep in int_model_deps.inner:
                if int_model_dep.PerfConfigs is not None:
                    for perf_cfg in int_model_dep.PerfConfigs:
                        model_sku_batching_configs.append(
                            ModelSKUBatchingConfig.make(
                                int_model_deps.Name,
                                int_model_deps.Protocol,
                                int_model_dep.TrafficType,
                                int_model_dep.Version,
                                perf_cfg.InstanceType,
                                perf_cfg.BatchingConfig.MaxBatchSize,
                                perf_cfg.BatchingConfig.IdleBatchSize,
                                perf_cfg.BatchingConfig.MaxBatchInterval,
                            )
                        )
        return ModelSKUBatchingConfigTable(model_sku_batching_configs)

    def validate_config_changes(self, prev: ModelSKUBatchingConfigTable):
        for curr_record in self.records:
            try:
                prev_record = prev.get_record(*curr_record.pk)
                curr_record.validate_config_changes(prev_record)
            except:
                continue


@typechecked
class ModelDeployment(Record):
    ATTRS = [
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, True, False),
        Attribute("Description", str, False, False),
        Attribute("CodeConfig", CodeConfig, False, True),
        Attribute("MaxConcurrentRequestsPerInstance", int, False, False),
        Attribute("EnvironmentConfig", EnvironmentConfig, False, False),
        Attribute("ModelConfig", ModelConfig, False, True),
    ]

    def validate_config_changes(self, prev: ModelDeployment):
        if self.CodeConfig is None:
            assert prev.CodeConfig is None, f"'CodeConfig' deleted from configuration."
        else:
            assert prev.CodeConfig is not None, f"'CodeConfig' added to configuration."
            try:
                self.CodeConfig.validate_config_changes(prev.CodeConfig)
            except Exception as ex:
                raise AssertionError(
                    f"Error while validating changes to CodeConfig. Error: {ex}"
                )
        assert (
            self.MaxConcurrentRequestsPerInstance
            == prev.MaxConcurrentRequestsPerInstance
        ), f"Current and previous MaxConcurrentRequestsPerInstance values must be equal."
        try:
            self.EnvironmentConfig.validate_config_changes(prev.EnvironmentConfig)
        except Exception as ex:
            raise AssertionError(
                f"Error while validating changes to EnvironmentConfig. Error: {ex}"
            )
        if self.ModelConfig is None:
            assert (
                prev.ModelConfig is None
            ), f"'ModelConfig' deleted from configuration."
        else:
            assert (
                prev.ModelConfig is not None
            ), f"'ModelConfig' added to configuration."
            try:
                self.ModelConfig.validate_config_changes(prev.ModelConfig)
            except Exception as ex:
                raise AssertionError(
                    f"Error while validating changes to ModelConfig. Error: {ex}"
                )

    def validate_in_ctx(self, sa_cfg: Optional[StorageAccountConfig]):
        if (
            (self.CodeConfig is not None)
            or (self.ModelConfig is not None)
            or (self.EnvironmentConfig.CondaFileConfig is not None)
        ):
            assert (
                sa_cfg is not None
            ), "StorageAccountConfig must be defined iff endpoint is configured with CodeConfig, ModelConfig, or CondaFileConfig."
        else:
            assert (
                sa_cfg is None
            ), "StorageAccountConfig must be defined iff endpoint is configured with CodeConfig, ModelConfig, or CondaFileConfig"


@typechecked
class ModelDeploymentTable(Table):
    RECORD_TYPE = ModelDeployment

    @staticmethod
    def make_from_int_model_dep_table(
        int_model_dep_table: IntModelDeploymentTable, model_ep_table: ModelEndpointTable
    ) -> ModelDeploymentTable:
        model_deps = []
        for int_model_deps in int_model_dep_table._inner:
            for int_model_dep in int_model_deps.inner:
                model_deps.append(
                    ModelDeployment.make(
                        int_model_deps.Name,
                        int_model_deps.Protocol,
                        int_model_dep.TrafficType,
                        int_model_dep.Version,
                        int_model_dep.Description,
                        int_model_dep.CodeConfig,
                        int_model_dep.MaxConcurrentRequestsPerInstance,
                        int_model_dep.EnvironmentConfig,
                        int_model_dep.ModelConfig,
                    )
                )
        model_dep_table = ModelDeploymentTable(model_deps)
        model_dep_table.validate_in_ctx(model_ep_table)
        return model_dep_table

    # def _validate_records(self):
    #     # TODO: unsuppress after implementing env vars. blocked by TextCopyright
    #     self._assert_no_dup_contents()

    def validate_config_changes(self, prev: ModelDeploymentTable):
        for curr_record in self.records:
            try:
                try:
                    prev_record = prev.get_record(*curr_record.pk)
                except Exception as ex:
                    logging.warning(ex)
                    continue
                curr_record.validate_config_changes(prev_record)
            except:
                raise RuntimeError(
                    f"Error while validating changes to model deployment with primary key {curr_record.pk}. Error: {ex}"
                )

    def validate_in_ctx(self, model_ep_table: ModelEndpointTable):
        for model_dep in self.records:
            model_ep: ModelEndpoint = model_ep_table.get_record(
                model_dep.Name, model_dep.Protocol
            )
            sa_cfg = None
            if model_ep.RemoteConfig is not None:
                sa_cfg = model_ep.RemoteConfig.StorageAccountConfig
            model_dep.validate_in_ctx(sa_cfg)


# DEPLOYMENT TARGET CONFIGURATION.
@typechecked
class MirrorTrafficTarget(Serializable):
    def __init__(self, Environment: Environment, Instance: int, Region: Region):
        self.Environment = Environment
        self.Instance = Instance
        self.Region = Region


class MirrorTrafficTargetSchema(IntSchema):
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region

    @validates_schema
    def validates_schema(self, data, **kwargs):
        env = Environment(data["Environment"])
        assert (
            env != Environment.PROD
        ), "Cannot forward mirrored traffic to PROD endpoints."
        assert not (
            env == Environment.PPE
            and data["Instance"] == 0
            and Region(data["Region"]) == Region.CENTRALUS
        ), f"Cannot forward mirrored traffic to PPE 0 CUS since it's used for A/B testing."

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        return MirrorTrafficTarget(**data)


@typechecked
class IntModelDeploymentState(Serializable):
    def __init__(
        self,
        Version: int,
        InstanceType: InstanceType,
        TrafficType: TrafficType = TrafficType.LIVE,
        TrafficPercentage: Optional[int] = 100,
        MirrorTrafficTarget: Optional[MirrorTrafficTarget] = None,
    ):
        self.TrafficType = TrafficType
        self.Version = Version
        self.InstanceType = InstanceType
        self.TrafficPercentage = TrafficPercentage
        self.MirrorTrafficTarget = MirrorTrafficTarget


class IntModelDeploymentStateSchema(IntSchema):
    TrafficType = CommonSchemas.TrafficType
    Version = CommonSchemas.Version
    InstanceType = CommonSchemas.InstanceType
    TrafficPercentage = fields.Int(
        validate=validate.Range(min=0, max=50),
        metadata={"description": "Total traffic percentage to allocate."},
    )
    # TODO: remove once model dep env vars implemented
    MirrorTrafficTarget = fields.Nested(MirrorTrafficTargetSchema, unknown=RAISE)

    @validates_schema
    def validates_schema(self, data, **kwargs):
        traffic_pct = data.get("TrafficPercentage")
        mirror_Traffic_target = data.get("MirrorTrafficTarget")
        if "TrafficType" in data:
            assert (
                TrafficType[data["TrafficType"]] == TrafficType.MIRROR
            ), "Only set TrafficType when configuring a deployment for mirror traffic. TrafficType is assumed to be LIVE otherwise."
            assert (
                traffic_pct is not None and mirror_Traffic_target is not None
            ), "TrafficPercentage and MirrorTrafficTarget must be defined iff configuring deployment with mirrored traffic."
        else:
            assert (
                traffic_pct is None and mirror_Traffic_target is None
            ), "TrafficPercentage and MirrorTrafficTarget must be defined iff configuring deployment with mirrored traffic."

    @post_load
    def make(self, data, **kwargs):
        if "TrafficType" in data:
            data["TrafficType"] = TrafficType[data["TrafficType"]]
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return IntModelDeploymentState(**data)


@typechecked
class IntModelEndpointState(Serializable):
    def __init__(
        self,
        Name: str,
        ModelDeploymentStates: List[IntModelDeploymentState],
        Protocol: Protocol = Protocol.HTTP,
        Auth: Auth = Auth.AAD,
    ):
        self.Name = Name
        self.Protocol = Protocol
        self.Auth = Auth
        self.ModelDeploymentStates = set(ModelDeploymentStates)


class IntModelEndpointStateSchema(IntSchema):
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Auth = CommonSchemas.Auth
    ModelDeploymentStates = fields.Nested(
        IntModelDeploymentStateSchema, required=True, many=True, unknown=RAISE
    )

    @validates("ModelDeploymentStates")
    @validate_elements(IntModelDeploymentStateSchema)
    def validate_model_dep_states(self, model_dep_states: List[ModelDeploymentState]):
        assert (
            len(model_dep_states) > 0
        ), "Must specify at least one ModelDeploymentState."
        # Not sorting by TrafficType since conflicts with sorting logic for
        # deployment-target-configs

    @validates_schema
    def validates_schema(self, data, **kwargs):
        if "Protocol" in data:
            assert (
                Protocol[data["Protocol"]] == Protocol.GRPC
            ), "Only set Protocol if value is GRPC. Protocol is assumed to be HTTP otherwise."
        if "Auth" in data:
            assert (
                Auth[data["Auth"]] == Auth.KEY
            ), "Only set Auth if value is 'KEY'. Auth is assumed to be 'AAD' otherwise."

    @post_load
    def make(self, data, **kwargs):
        if "Protocol" in data:
            data["Protocol"] = Protocol[data["Protocol"]]
        if "Auth" in data:
            data["Auth"] = Auth[data["Auth"]]
        return IntModelEndpointState(**data)


@typechecked
class AsyncAgentConfig(Serializable):
    def __init__(self, ImageTag: str, OrchConcurrency: int):
        self.ImageTag = ImageTag
        self.OrchConcurrency = OrchConcurrency

    def validate_in_ctx(self, work_queue_eh_partition_count: int):
        assert (
            self.OrchConcurrency % work_queue_eh_partition_count == 0
        ), f"Orchestrator concurrency {self.OrchConcurrency} is not integer divisible by {work_queue_eh_partition_count}."


class AsyncAgentConfigSchema(IntSchema):
    ImageTag = fields.Str(required=True, validate=validate.Length(min=1))
    OrchConcurrency = fields.Int(required=True, validate=validate.Range(min=1))

    @post_load
    def make(self, data, **kwargs):
        return AsyncAgentConfig(**data)


@typechecked
class AlertAgentConfig(Serializable):
    def __init__(self, ImageTag: str):
        self.ImageTag = ImageTag


@typechecked
class ServiceAlertAgentConfig(AlertAgentConfig):
    pass


class AlertAgentConfigSchema(IntSchema):
    ImageTag = fields.Str(required=True, validate=validate.Length(min=1))


class ServiceAlertAgentConfigSchema(AlertAgentConfigSchema):
    @post_load
    def make(self, data, **kwargs):
        return ServiceAlertAgentConfig(**data)


@typechecked
class DeploymentTargetConfig(Serializable):
    def __init__(
        self,
        Environment: Environment,
        Instance: int,
        Region: Region,
        ModelEndpointStates: List[IntModelEndpointState],
        AsyncAgentConfig: AsyncAgentConfig,
        ServiceAlertAgentConfig: ServiceAlertAgentConfig,
    ):
        self.Environment = Environment
        self.Instance = Instance
        self.Region = Region
        self.ModelEndpointStates = set(ModelEndpointStates)
        self.AsyncAgentConfig = AsyncAgentConfig
        self.ServiceAlertAgentConfig = ServiceAlertAgentConfig


class IntDeploymentTargetConfigSchema(IntSchema):
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    ModelEndpointStates = fields.Nested(
        IntModelEndpointStateSchema, required=True, many=True, unknown=RAISE
    )
    AsyncAgentConfig = fields.Nested(
        AsyncAgentConfigSchema, required=True, unknown=RAISE
    )
    ServiceAlertAgentConfig = fields.Nested(
        ServiceAlertAgentConfigSchema, required=True, unknown=RAISE
    )

    @validates("ModelEndpointStates")
    @validate_elements(IntModelEndpointStateSchema)
    def validate_model_ep_states(self, model_ep_states: List[IntModelEndpointState]):
        assert model_ep_states == sorted(
            model_ep_states, key=lambda x: (x.Name.lower(), x.Protocol, x.Auth)
        ), "Model endpoint states must be sorted alphabetically then by Protocol (HTTP before GRPC) and Auth (AAD before KEY)."

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        return DeploymentTargetConfig(**data)


@typechecked
class IntDeploymentTargetConfigTable:
    def __init__(self, inner: List[DeploymentTargetConfig]):
        self.inner = set(inner)

    @staticmethod
    def make(dir_path: PosixPath) -> IntDeploymentTargetConfigTable:
        dep_target_cfgs = []
        for env_dir_path in dir_path.iterdir():
            for dep_target_cfg_file_path in env_dir_path.iterdir():
                with open(dep_target_cfg_file_path, "r") as f:
                    dep_target_cfg = IntDeploymentTargetConfigSchema(
                        unknown=RAISE
                    ).load(json.load(f))
                dep_target_cfgs.append(dep_target_cfg)
        return IntDeploymentTargetConfigTable(dep_target_cfgs)

    # TODO: remove once tables created for Async and Alert agents
    def get_record(
        self, env: Environment, instance: int, region: Region
    ) -> DeploymentTargetConfig:
        for cfg in self.inner:
            if (
                cfg.Environment == env
                and cfg.Instance == instance
                and cfg.Region == region
            ):
                return cfg
        raise RuntimeError(
            f"Unable to find deployment target configuration record with primary key {(env, instance, region)}."
        )

    # TODO: revisit
    # def make_subset_from_envs(
    #     self, envs: Set[Environment]
    # ) -> DeploymentTargetConfigSet:
    #     return DeploymentTargetConfigSet(
    #         [cfg for cfg in self.configs if cfg.Environment in envs]
    #     )


# TEMP: Will delete with CD state machine update
@typechecked
class AmlEndpointConfig:
    def __init__(
        self,
        model_ep: ModelEndpoint,
        auth: Auth,
        env: Environment,
        instance: int,
    ):
        self.base_name = model_ep.Name
        self.auth = auth
        self.env = env
        self.name = AmlEndpointConfig.make_name(
            self.base_name, model_ep.Protocol, auth, env, instance
        )
        self.cfg = model_ep
        self._pre_existing = None

    @property
    def pre_existing(self) -> bool:
        if self._pre_existing is None:
            raise RuntimeError("Must first determine whether endpoint is pre-existing.")
        return self._pre_existing

    @pre_existing.setter
    def pre_existing(self, result: bool):
        self._pre_existing = result

    @staticmethod
    def make_base_url(name: str, region: Region, protocol: Protocol) -> str:
        return f"{protocol.value.lower()}s://{AmlEndpointConfig.make_hostname(name, region)}"

    @staticmethod
    def make_name(
        model_name: str, protocol: Protocol, auth: Auth, env: Environment, instance: int
    ) -> str:
        name = f"rai-{model_name}"
        if protocol == Protocol.GRPC:
            name += "-grpc"
        if auth == Auth.KEY:
            name += "-key"
        name += f"-{env}"
        if instance != 0:
            name += f"-{instance}"
        return name.lower()

    @staticmethod
    def make_hostname(name: str, region: Region) -> str:
        return f"{name}.{region.value.lower()}.inference.ml.azure.com"


@typechecked
class Cluster(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
    ]


@typechecked
class ClusterTable(Table):
    RECORD_TYPE = Cluster

    @staticmethod
    def make_from_int_dep_target_cfg_table(
        int_dep_target_cfg_table: IntDeploymentTargetConfigTable,
    ) -> ClusterTable:
        return ClusterTable(
            [
                Cluster.make(cfg.Environment, cfg.Instance, cfg.Region)
                for cfg in int_dep_target_cfg_table.inner
            ]
        )


@typechecked
class ModelEndpointState(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("Auth", Auth, True, False),
    ]

    def make_from_arm_json(
        environment: Environment, instance: int, region: Region, ep_show_info: Dict
    ) -> ModelEndpointState:
        ep_tags = ep_show_info["tags"]
        return ModelEndpointState.make(
            environment,
            instance,
            region,
            ep_tags["model"],
            Protocol[ep_tags["protocol"].upper()],
            Auth[ep_tags["auth"].upper()],
        )


@typechecked
class ModelEndpointStateTable(Table):
    RECORD_TYPE = ModelEndpointState

    @staticmethod
    def make_from_int_dep_target_cfg_table(
        int_dep_target_cfg_table: IntDeploymentTargetConfigTable,
        model_ep_table: ModelEndpointTable,
    ) -> ModelEndpointStateTable:
        model_ep_states = []
        for dep_target_cfg in int_dep_target_cfg_table.inner:
            for model_ep_state in dep_target_cfg.ModelEndpointStates:
                model_ep_states.append(
                    ModelEndpointState.make(
                        dep_target_cfg.Environment,
                        dep_target_cfg.Instance,
                        dep_target_cfg.Region,
                        model_ep_state.Name,
                        model_ep_state.Protocol,
                        model_ep_state.Auth,
                    )
                )
        model_ep_state_table = ModelEndpointStateTable(model_ep_states)
        model_ep_state_table.validate_in_ctx(model_ep_table)
        return model_ep_state_table

    def validate_in_ctx(self, model_ep_table: ModelEndpointTable):
        for model_ep_state in self.records:
            model_ep_table.get_record(model_ep_state.Name, model_ep_state.Protocol)


@typechecked
class ModelDeploymentState(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("Auth", Auth, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, False, False),
        Attribute("InstanceType", InstanceType, False, False),
        Attribute("TrafficPercentage", int, False, False),
        Attribute("MirrorTrafficTarget", MirrorTrafficTarget, False, True),
    ]

    @staticmethod
    def make_from_arm_json(
        model_ep_state: ModelEndpointState, dep_show_info: Dict
    ) -> ModelDeploymentState:
        dep_tags = dep_show_info["tags"]
        return ModelDeploymentState.make(
            model_ep_state.Environment,
            model_ep_state.Instance,
            model_ep_state.Region,
            model_ep_state.Name,
            model_ep_state.Protocol,
            model_ep_state.Auth,
            TrafficType[dep_tags["traffic_type"]],
            int(dep_tags["version"]),
            InstanceType[dep_show_info["instance_type"].upper()],
            int(dep_tags["traffic_percentage"]),
            None,
        )

    def _validate(self):
        # NOTE: Temporary check on None, as setting MirrorTrafficTarget to None while loading output csvs
        if (
            self.TrafficType == TrafficType.MIRROR
            and self.MirrorTrafficTarget is not None
        ):
            # TODO: Current logic checks that no endpoint in region-env-instance
            # of currently deployed cluster will forward mirrored traffic to another
            # endpoint in that same region, environment, and instance. It does NOT
            # verify that no loops exist between mirror traffic configurations
            # across different region-env-instances (e.g. eastus PPE 0 gRPC
            # orchestrator forwards mirrored traffic to centralus PPE 1 gRPC
            # orchestrator, which forwards traffic to eastus PPE 0 gRPC
            # orchestrator)
            assert not (
                self.Environment == self.MirrorTrafficTarget.Environment
                and self.Instance == self.MirrorTrafficTarget.Instance
                and self.Region == self.MirrorTrafficTarget.Region
            ), f"Cannot forward mirrored traffic to endpoint in same cluster."


class ModelDeploymentStateSchema(IntSchema):
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Auth = CommonSchemas.Auth
    TrafficType = CommonSchemas.TrafficType
    Version = CommonSchemas.Version
    InstanceType = CommonSchemas.InstanceType
    # TODO: remove once state machine updated
    TrafficPercentage = fields.Int(
        validate=validate.Range(min=0, max=100),
        metadata={"description": "Total traffic percentage to allocate."},
    )

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        data["Protocol"] = Protocol[data["Protocol"].upper()]
        data["Auth"] = Auth[data["Auth"].upper()]
        data["TrafficType"] = TrafficType[data["TrafficType"]]
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return ModelDeploymentState(**data)


@typechecked
class ModelDeploymentStateTable(Table):
    RECORD_TYPE = ModelDeploymentState

    @staticmethod
    def make_from_csv(file_path: PosixPath) -> ModelDeploymentStateTable:
        with open(file_path, "r") as f:
            return ModelDeploymentStateTable(
                ModelDeploymentStateSchema(many=True, unknown=EXCLUDE).load(
                    csv.DictReader(f)
                )
            )

    @staticmethod
    def make_from_int_dep_target_cfg_table(
        int_dep_target_cfg_table: IntDeploymentTargetConfigTable,
        model_dep_table: ModelDeploymentTable,
        deployed_sku_limits_table: DeployedSKULimitsTable,
        model_sku_batching_config_table: ModelSKUBatchingConfigTable,
    ) -> ModelDeploymentStateTable:
        model_dep_states = []
        for dep_target_cfg in int_dep_target_cfg_table.inner:
            for model_ep_state in dep_target_cfg.ModelEndpointStates:
                for model_dep_state in model_ep_state.ModelDeploymentStates:
                    model_dep_states.append(
                        ModelDeploymentState.make(
                            dep_target_cfg.Environment,
                            dep_target_cfg.Instance,
                            dep_target_cfg.Region,
                            model_ep_state.Name,
                            model_ep_state.Protocol,
                            model_ep_state.Auth,
                            model_dep_state.TrafficType,
                            model_dep_state.Version,
                            model_dep_state.InstanceType,
                            model_dep_state.TrafficPercentage,
                            model_dep_state.MirrorTrafficTarget,
                        )
                    )
        model_dep_state_table = ModelDeploymentStateTable(model_dep_states)
        model_dep_state_table.validate_in_ctx(
            model_dep_table, deployed_sku_limits_table, model_sku_batching_config_table
        )
        return model_dep_state_table

    def validate_in_ctx(
        self,
        model_dep_table: ModelDeploymentTable,
        deployed_sku_limits_table: DeployedSKULimitsTable,
        model_sku_batching_config_table: ModelSKUBatchingConfigTable,
    ):
        for model_dep_state in self.records:
            model_dep_table.get_record(
                model_dep_state.Name,
                model_dep_state.Protocol,
                model_dep_state.TrafficType,
                model_dep_state.Version,
            )
            # If model deployment has any batching configuration configured,
            # then it must have one configured with model deployment state's
            # instance type.
            if (
                model_sku_batching_config_table.filter_by_pks(
                    **{
                        "Name": model_dep_state.Name,
                        "Protocol": model_dep_state.Protocol,
                        "TrafficType": model_dep_state.TrafficType,
                        "Version": model_dep_state.Version,
                    }
                ).records
                != []
            ):
                model_sku_batching_config_table.get_record(
                    model_dep_state.Name,
                    model_dep_state.Protocol,
                    model_dep_state.TrafficType,
                    model_dep_state.Version,
                    model_dep_state.InstanceType,
                )
            deployed_sku_limits_table.get_record(
                model_dep_state.Environment,
                model_dep_state.Instance,
                model_dep_state.Region,
                model_dep_state.InstanceType,
            )

    def _validate_records(self):
        traffic_type_map = {}
        partial_pks = set()
        for model_dep_state in self.records:
            pk = model_dep_state.pk
            partial_pk = pk[:-1]
            if partial_pk not in traffic_type_map:
                traffic_type_map[partial_pk] = {
                    TrafficType.LIVE: False,
                    TrafficType.MIRROR: False,
                }
            traffic_type_map[partial_pk][pk[-1]] = True
            partial_pks.add(partial_pk)
        for partial_pk in partial_pks:
            if (
                traffic_type_map[partial_pk][TrafficType.MIRROR]
                and not traffic_type_map[partial_pk][TrafficType.LIVE]
            ):
                raise RuntimeError(
                    f"Cannot configure model deployment state with partial primary key {partial_pk} and traffic type 'MIRROR' unless also configuring state with same partial primary key and traffic type 'LIVE'."
                )


@typechecked
class ModelDeploymentInstanceState(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("Auth", Auth, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("DepInstance", int, True, False),
        Attribute("InstanceCount", int, False, False),
        # TODO: remove once state machine updated
        Attribute("TrafficPercentage", int, False, False),
        # TODO: remove once model dep env vars implemented
        Attribute("MirrorTrafficTarget", MirrorTrafficTarget, False, True),
    ]

    @staticmethod
    def make_from_arm_json(
        model_endpoint_state: ModelEndpointState, dep_show_info: Dict
    ) -> ModelDeploymentInstanceState:
        dep_tags = dep_show_info["tags"]
        return ModelDeploymentInstanceState.make(
            model_endpoint_state.Environment,
            model_endpoint_state.Instance,
            model_endpoint_state.Region,
            model_endpoint_state.Name,
            model_endpoint_state.Protocol,
            model_endpoint_state.Auth,
            TrafficType[dep_tags["traffic_type"]],
            int(dep_tags["version"]),
            InstanceType[dep_show_info["instance_type"].upper()],
            int(dep_tags["instance"]),
            int(dep_show_info["instance_count"]),
            100,  # passing hard coded value as these values doesn't matter as they are temporary fields
            None,
        )


class ModelDeploymentInstanceStateSchema(IntSchema):
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Auth = CommonSchemas.Auth
    TrafficType = CommonSchemas.TrafficType
    Version = CommonSchemas.Version
    InstanceType = CommonSchemas.InstanceType
    DepInstance = fields.Int(
        required=True,
        validate=validate.Range(min=0),
    )
    InstanceCount = fields.Int(required=True, validate=validate.Range(min=1))
    # TODO: remove once state machine updated
    TrafficPercentage = fields.Int(
        validate=validate.Range(min=0, max=100),
        metadata={"description": "Total traffic percentage to allocate."},
    )

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        data["Protocol"] = Protocol[data["Protocol"].upper()]
        data["Auth"] = Auth[data["Auth"].upper()]
        data["TrafficType"] = TrafficType[data["TrafficType"]]
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return ModelDeploymentInstanceState(**data)


@typechecked
class ModelDeploymentInstanceStateTable(Table):
    RECORD_TYPE = ModelDeploymentInstanceState

    @staticmethod
    def compute_mdis_instance_counts(
        traffic_type: TrafficType,
        instance_count: int,
        max_instances_per_dep: int,
        traffic_percentage: int,  # TODO: delete
    ) -> List[Tuple[int, int]]:
        # TEMP: Front-load instances to deployments until state machine
        # updated.
        dep_instance_counts = []
        instance_count_remaining = instance_count
        while instance_count_remaining > 0:
            dep_instance_count = (
                instance_count_remaining
                if traffic_type == TrafficType.MIRROR
                else min(max_instances_per_dep, instance_count_remaining)
            )
            dep_instance_counts.append(dep_instance_count)
            instance_count_remaining -= dep_instance_count
        # END TEMP

        # num_deps = (
        #     1
        #     if traffic_type == TrafficType.MIRROR
        #     else math.ceil(instance_count / max_instances_per_dep)
        # )
        # instances_per_dep, remainder = divmod(instance_count, num_deps)
        # dep_instance_counts = [instances_per_dep] * num_deps
        # iidx = 0
        # while iidx < remainder:
        #     dep_instance_counts[iidx] += 1
        #     iidx += 1

        # TEMP: Assign traffic percentage to each model deployment instance
        # until state machine updated.
        traffic_remaining = traffic_percentage
        dep_traffic_percentages = []
        for dep_instance_count in dep_instance_counts:
            instance_traffic = int(
                round(traffic_percentage * dep_instance_count / instance_count)
            )
            dep_traffic_percentages.append(instance_traffic)
            traffic_remaining -= instance_traffic

        # Distribute remaining or collect excess traffic.
        for iidx in range(len(dep_traffic_percentages)):
            if traffic_remaining > 0:
                dep_traffic_percentages[iidx] += 1
                traffic_remaining -= 1
            elif traffic_remaining < 0:
                dep_traffic_percentages[iidx] -= 1
                traffic_remaining += 1
            else:
                break
        assert (
            sum(dep_traffic_percentages) == traffic_percentage
        ), f"Total traffic percentage across all model deployment instances must equal {traffic_percentage}. Total: {sum(dep_traffic_percentages)}"
        # END TEMP

        mdis_instance_counts = []
        for iidx in range(len(dep_instance_counts)):
            result = (dep_instance_counts[iidx], dep_traffic_percentages[iidx])
            mdis_instance_counts.append(result)
        return mdis_instance_counts

    @staticmethod
    def make_from_csv(file_path: PosixPath) -> ModelDeploymentInstanceStateTable:
        with open(file_path, "r") as f:
            return ModelDeploymentInstanceStateTable(
                ModelDeploymentInstanceStateSchema(many=True, unknown=EXCLUDE).load(
                    csv.DictReader(f)
                )
            )

    @staticmethod
    def make(
        model_dep_state_table: ModelDeploymentStateTable,
        model_dep_perf_table: ModelDeploymentPerfTable,
        model_load_cfg_table: ModelLoadConfigTable,
        deployed_sku_limits_table: DeployedSKULimitsTable,
    ) -> ModelDeploymentInstanceStateTable:
        mdi_states = []
        for rec in model_dep_state_table.records:
            rps_per_instance = model_dep_perf_table.get_record(
                rec.Environment,
                rec.Instance,
                rec.Region,
                rec.Name,
                rec.Protocol,
                rec.TrafficType,
                rec.Version,
                rec.InstanceType,
            ).RPSPerInstance
            filtered_model_load_cfg_table = model_load_cfg_table.filter_by_pks(
                **{
                    "Environment": rec.Environment,
                    "Instance": rec.Instance,
                    "Region": rec.Region,
                    "Name": rec.Name,
                    "Protocol": rec.Protocol,
                    "Auth": rec.Auth,
                }
            )
            # TODO: add option to skip async traffic
            total_rps = (
                sum([mlc_rec.RPS for mlc_rec in filtered_model_load_cfg_table.records])
                * rec.TrafficPercentage
                / 100
            )
            instance_count = math.ceil(total_rps / rps_per_instance)
            deployed_sku_limits = deployed_sku_limits_table.get_record(
                rec.Environment, rec.Instance, rec.Region, rec.InstanceType
            )
            instance_count = max(instance_count, deployed_sku_limits.MinInstanceCount)
            min_max_instances_per_dep = deployed_sku_limits.MinMaxInstancesPerDep
            # No more than 20 deployment instances behind each endpoint.
            # TEMP: set limit to 20/2 since still deploy with blue-green
            max_instances_per_dep = min_max_instances_per_dep * math.ceil(
                instance_count / (10 * min_max_instances_per_dep)
            )
            mdis_instance_counts = (
                ModelDeploymentInstanceStateTable.compute_mdis_instance_counts(
                    rec.TrafficType,
                    instance_count,
                    max_instances_per_dep,
                    rec.TrafficPercentage,
                )
            )
            for iidx in range(len(mdis_instance_counts)):
                mdi_states.append(
                    ModelDeploymentInstanceState.make(
                        rec.Environment,
                        rec.Instance,
                        rec.Region,
                        rec.Name,
                        rec.Protocol,
                        rec.Auth,
                        rec.TrafficType,
                        rec.Version,
                        rec.InstanceType,
                        iidx,
                        mdis_instance_counts[iidx][0],
                        mdis_instance_counts[iidx][1],
                        rec.MirrorTrafficTarget,
                    )
                )
        return ModelDeploymentInstanceStateTable(mdi_states)


# DEPLOYED SKU LIMITS.
@typechecked
class IntDeployedSKULimits(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, True),
        Attribute("Instance", int, True, True),
        Attribute("Region", Region, True, True),
        Attribute("InstanceType", InstanceType, True, True),
        Attribute("MinInstanceCount", int, False, True),
        Attribute("MinMaxInstancesPerDep", int, False, True),
    ]

    def _validate(self):
        assert (
            self.MinInstanceCount is not None or self.MinMaxInstancesPerDep is not None
        ), "Must specify at least one of MinInstanceCount or MinMaxInstancesPerDep."


class IntDeployedSKULimitsSchema(IntSchema):
    Environment = fields.Str(validate=validate.OneOf([e.value for e in Environment]))
    Instance = CommonSchemas.OptInstance
    Region = fields.Str(validate=validate.OneOf([r.value for r in Region]))
    InstanceType = fields.Str(validate=validate.OneOf([i.value for i in InstanceType]))
    MinInstanceCount = fields.Int(validate=validate.Range(min=1))
    MinMaxInstancesPerDep = fields.Int(validate=validate.Range(min=1))

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        opt_keys = [
            "Environment",
            "Instance",
            "Region",
            "InstanceType",
            "MinInstanceCount",
            "MinMaxInstancesPerDep",
        ]
        for key in opt_keys:
            if data[key] == "":
                data.pop(key)
        return data

    @post_load
    def make(self, data, **kwargs):
        if "Environment" in data:
            data["Environment"] = Environment(data["Environment"])
        if "Region" in data:
            data["Region"] = Region(data["Region"])
        if "InstanceType" in data:
            data["InstanceType"] = InstanceType(data["InstanceType"])
        return IntDeployedSKULimits(**data)


@typechecked
class IntDeployedSKULimitsTable(Table):
    RECORD_TYPE = IntDeployedSKULimits

    @staticmethod
    def make(file_path: PosixPath) -> IntDeployedSKULimitsTable:
        with open(file_path, "r") as f:
            return IntDeployedSKULimitsTable(
                IntDeployedSKULimitsSchema(many=True, unknown=RAISE).load(
                    csv.DictReader(f)
                )
            )

    def make_deployed_sku_limits_record(
        self, partial_dsl_record: IntDeployedSKULimits
    ) -> DeployedSKULimits:
        # Search for MinInstanceCount and MinMaxInstancesPerDep values with which
        # to populate DeployedSKULimits record with following strategy.
        # (1) If intermediate record with exact primary key exists, permanently
        # assign value(s).
        # (2) If intermediate record with one or more optional component primary
        # keys exist, assign value(s) if smaller than current.
        # (3) If intermediate record with no primary key exists, assign value(s)
        # if smaller than current and current value(s) were not assigned by (2).
        # (4) If both values are unassigned after iterating across all
        # intermediate records, raise error.
        def update_info(curr, rec_value, any_opt_pks_match):
            if rec_value is None or curr[2]:
                pass
            elif curr[0] == 0 or (any_opt_pks_match and not curr[1]):
                curr[0] = rec_value
                curr[1] = any_opt_pks_match
            elif (curr[1] and any_opt_pks_match) or not curr[1]:
                curr[0] = min(curr[0], rec_value)

        # Stores value, whether any optional primary keys matched when assigning
        # value, and whether value assignment is permanent.
        try:
            idsl_record = self.get_record(partial_dsl_record.pk)
            if idsl_record.MinInstanceCount is not None:
                min_instance_ct_info = [idsl_record.MinInstanceCount, True, True]
            if idsl_record.MinMaxInstancesPerDep is not None:
                min_max_instances_per_dep_info = [
                    idsl_record.MinMaxInstancesPerDep,
                    True,
                    True,
                ]
        except:
            min_instance_ct_info = [0, False, False]
            min_max_instances_per_dep_info = [0, False, False]
        for rec in self.records:
            if any(
                getattr(rec, attr) != getattr(partial_dsl_record, attr)
                for attr in self._pk_attr_names
                if getattr(rec, attr) is not None
            ):
                continue
            any_opt_pks_match = any(
                getattr(rec, attr) == getattr(partial_dsl_record, attr)
                for attr in self._pk_attr_names
                if getattr(rec, attr) is not None
            )
            update_info(min_instance_ct_info, rec.MinInstanceCount, any_opt_pks_match)
            update_info(
                min_max_instances_per_dep_info,
                rec.MinMaxInstancesPerDep,
                any_opt_pks_match,
            )
        if min_instance_ct_info[0] == 0 or min_max_instances_per_dep_info[0] == 0:
            raise RuntimeError(
                f"Unable to assign MinInstanceCount and MinMaxInstancesPerDep values for deployed SKU limits record with primary key {partial_dsl_record.pk} after searching intermediate records."
            )
        return DeployedSKULimits.make(
            partial_dsl_record.Environment,
            partial_dsl_record.Instance,
            partial_dsl_record.Region,
            partial_dsl_record.InstanceType,
            min_instance_ct_info[0],
            min_max_instances_per_dep_info[0],
        )


@typechecked
class DeployedSKULimits(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("MinInstanceCount", int, False, False),
        Attribute("MinMaxInstancesPerDep", int, False, False),
    ]


@typechecked
class DeployedSKULimitsTable(Table):
    RECORD_TYPE = DeployedSKULimits

    @staticmethod
    def make(
        file_path: PosixPath, cluster_table: ClusterTable
    ) -> DeployedSKULimitsTable:
        int_deployed_sku_limits_table = IntDeployedSKULimitsTable.make(file_path)
        # Make deployed SKU limits record for each configured model
        # deployment.
        dsl_records = set()
        for cluster_record in cluster_table.records:
            for instance_type in InstanceType:
                idsl_record = IntDeployedSKULimits.make(
                    cluster_record.Environment,
                    cluster_record.Instance,
                    cluster_record.Region,
                    instance_type,
                    0,
                    0,
                )
                dsl_records.add(
                    int_deployed_sku_limits_table.make_deployed_sku_limits_record(
                        idsl_record
                    )
                )
        return DeployedSKULimitsTable(list(dsl_records))


# MODEL DEPLOYMENT PERFORMANCE.
@typechecked
class IntModelDeploymentPerf(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, True),
        Attribute("Instance", int, True, True),
        Attribute("Region", Region, True, True),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, True, True),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("RPSPerInstance", float, False, False),
        Attribute("Description", str, False, True),
    ]


class IntModelDeploymentPerfSchema(IntSchema):
    Environment = fields.Str(validate=validate.OneOf([e.value for e in Environment]))
    Instance = CommonSchemas.OptInstance
    Region = fields.Str(validate=validate.OneOf([r.value for r in Region]))
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    TrafficType = CommonSchemas.TrafficType
    Version = fields.Int(validate=validate.Range(min=1))
    InstanceType = CommonSchemas.InstanceType
    RPSPerInstance = CommonSchemas.RPSPerInstance
    Description = CommonSchemas.OptString

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        for attr in ["Environment", "Instance", "Region", "Version", "Description"]:
            if data[attr] == "":
                data.pop(attr)
        return data

    @post_load
    def make(self, data, **kwargs):
        if "Environment" in data:
            data["Environment"] = Environment(data["Environment"])
        if "Region" in data:
            data["Region"] = Region(data["Region"])
        data["Protocol"] = Protocol[data["Protocol"]]
        data["TrafficType"] = TrafficType[data["TrafficType"]]
        data["InstanceType"] = InstanceType(data["InstanceType"])
        return IntModelDeploymentPerf(**data)


@typechecked
class IntModelDeploymentPerfTable(Table):
    RECORD_TYPE = IntModelDeploymentPerf

    @staticmethod
    def make(file_path: PosixPath) -> IntModelDeploymentPerfTable:
        with open(file_path, "r") as f:
            return IntModelDeploymentPerfTable(
                IntModelDeploymentPerfSchema(many=True, unknown=RAISE).load(
                    csv.DictReader(f)
                )
            )

    def make_model_dep_perf_record(
        self, partial_mdp_record: IntModelDeploymentPerf
    ) -> ModelDeploymentPerf:
        # Search for RPSPerInstance value with which to populate
        # ModelDeploymentPerf record with following strategy.
        # (1) If intermediate record with exact primary key exists, permanently
        # assign value.
        # (2) If intermediate record with mandatory component primary keys and
        # one or more optional component primary keys exist, assign value(s) if
        # smaller than current.
        # (3) If intermediate record with mandatory component primary keys
        # exist, assign value if smaller than current and current was not
        # assigned by (2).
        # (4) If no record with mandatory component primary keys exist, raise
        # error.
        def update_info(curr, rec_value, any_opt_pks_match):
            if rec_value is None or curr[2]:
                pass
            elif curr[0] == 0 or (any_opt_pks_match and not curr[1]):
                curr[0] = rec_value
                curr[1] = any_opt_pks_match
            elif (curr[1] and any_opt_pks_match) or not curr[1]:
                curr[0] = min(curr[0], rec_value)

        # Stores value, whether any optional primary keys matched when assigning
        # value, and whether value assignment is permanent.
        try:
            rps_per_instance_info = [
                self.get_record(partial_mdp_record.pk).RPSPerInstance,
                True,
                True,
            ]
        except:
            rps_per_instance_info = [0, False, False]
        for rec in self.records:
            if any(
                getattr(rec, attr) != getattr(partial_mdp_record, attr)
                for attr in self._pk_attr_names
                if getattr(rec, attr) is not None
            ):
                continue
            any_opt_pks_match = any(
                getattr(rec, attr) == getattr(partial_mdp_record, attr)
                for attr in self._opt_pk_attr_names
                if getattr(rec, attr) is not None
            )
            update_info(rps_per_instance_info, rec.RPSPerInstance, any_opt_pks_match)
        if rps_per_instance_info[0] == 0:
            raise RuntimeError(
                f"Unable to assign RPSPerInstance value for model deployment performance record with primary key {partial_mdp_record.pk} after searching intermediate records."
            )
        return ModelDeploymentPerf.make(
            partial_mdp_record.Environment,
            partial_mdp_record.Instance,
            partial_mdp_record.Region,
            partial_mdp_record.Name,
            partial_mdp_record.Protocol,
            partial_mdp_record.TrafficType,
            partial_mdp_record.Version,
            partial_mdp_record.InstanceType,
            rps_per_instance_info[0],
            partial_mdp_record.Description,
        )


@typechecked
class ModelDeploymentPerf(Record):
    ATTRS = [
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("TrafficType", TrafficType, True, False),
        Attribute("Version", int, True, False),
        Attribute("InstanceType", InstanceType, True, False),
        Attribute("RPSPerInstance", float, False, False),
        Attribute("Description", str, False, False),
    ]


@typechecked
class ModelDeploymentPerfTable(Table):
    RECORD_TYPE = ModelDeploymentPerf

    @staticmethod
    def make(
        file_path: PosixPath, model_dep_state_table: ModelDeploymentStateTable
    ) -> ModelDeploymentPerfTable:
        int_model_dep_perf_table = IntModelDeploymentPerfTable.make(file_path)
        # Make model deployment performance record for each configured model
        # deployment.
        mdp_records = set()
        for mds_record in model_dep_state_table.records:
            imdp_record = IntModelDeploymentPerf.make(
                mds_record.Environment,
                mds_record.Instance,
                mds_record.Region,
                mds_record.Name,
                mds_record.Protocol,
                mds_record.TrafficType,
                mds_record.Version,
                mds_record.InstanceType,
                0.0,
                "",
            )
            mdp_records.add(
                int_model_dep_perf_table.make_model_dep_perf_record(imdp_record)
            )
        return ModelDeploymentPerfTable(list(mdp_records))


# MODEL LOAD CONFIGURATION.
@typechecked
class ModelLoadConfig(Record):
    ATTRS = [
        Attribute("ObjectId", UUID, True, False),
        Attribute("ObjectCoarseId", str, True, True),
        Attribute("Environment", Environment, True, False),
        Attribute("Instance", int, True, False),
        Attribute("Region", Region, True, False),
        Attribute("Name", str, True, False),
        Attribute("Protocol", Protocol, True, False),
        Attribute("Auth", Auth, True, False),
        Attribute("Path", Path, True, False),
        Attribute("RPS", float, False, False),
        Attribute("Description", str, False, True),
    ]


class ModelLoadConfigSchema(IntSchema):
    ObjectId = fields.UUID(required=True)
    ObjectCoarseId = CommonSchemas.OptString
    Environment = CommonSchemas.Environment
    Instance = CommonSchemas.Instance
    Region = CommonSchemas.Region
    Name = CommonSchemas.Name
    Protocol = CommonSchemas.Protocol
    Auth = CommonSchemas.Auth
    Path = CommonSchemas.Path
    RPS = fields.Float(
        required=True, validate=validate.Range(min=0.0, min_inclusive=False)
    )
    Description = CommonSchemas.OptString

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["ObjectCoarseId"] == "":
            data.pop("ObjectCoarseId")
        if data["Description"] == "":
            data.pop("Description")
        return data

    @post_load
    def make(self, data, **kwargs):
        data["Environment"] = Environment(data["Environment"])
        data["Region"] = Region(data["Region"])
        data["Protocol"] = Protocol[data["Protocol"]]
        data["Auth"] = Auth[data["Auth"]]
        data["Path"] = Path[data["Path"]]
        return ModelLoadConfig(**data)


@typechecked
class ModelLoadConfigTable(Table):
    RECORD_TYPE = ModelLoadConfig

    @staticmethod
    def make(
        file_path: PosixPath,
        customer_table: CustomerTable,
        model_ep_state_table: ModelEndpointStateTable,
    ) -> ModelLoadConfigTable:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            data = []
            for row in reader:
                # Skip customer names. These will be deleted once load
                # configurations are automatically populated based on usage.
                if len([v for v in list(row.values()) if v != ""]) == 1:
                    continue

                # Allow Name to contain an array of model endpoint names to simplify
                # configuration for customers.
                for name in row["Name"].split(","):
                    row_copy = copy.deepcopy(row)
                    row_copy["Name"] = name.replace(" ", "")
                    data.append(row_copy)
        model_load_cfg_table = ModelLoadConfigTable(
            ModelLoadConfigSchema(many=True, unknown=RAISE).load(data)
        )
        for rec in model_load_cfg_table.records:
            customer_table.get_record(rec.ObjectId, rec.ObjectCoarseId)
            model_ep_state_table.get_record(
                rec.Environment,
                rec.Instance,
                rec.Region,
                rec.Name,
                rec.Protocol,
                rec.Auth,
            )
        return model_load_cfg_table


# REGIONS
@typechecked
class RegionRecord(Record):
    ATTRS = [
        Attribute("Name", Region, True, False),
        Attribute("Abbreviation", str, False, False),
        Attribute("AMLKustoCluster", str, False, True),
        Attribute("MhsmUri", str, False, True),
    ]


class RegionSchema(Schema):
    Name = CommonSchemas.Name
    Abbreviation = CommonSchemas.Name
    AMLKustoCluster = CommonSchemas.OptString
    MhsmUri = CommonSchemas.OptString

    @pre_load
    def pre_load(self, data, **kwargs) -> Dict[str, Any]:
        if data["AMLKustoCluster"] == "":
            data.pop("AMLKustoCluster")
        if data["MhsmUri"] == "":
            data.pop("MhsmUri")
        return data

    @post_load
    def make(self, data, **kwargs):
        data["Name"] = Region(data["Name"])
        return RegionRecord(**data)


@typechecked
class RegionTable(Table):
    RECORD_TYPE = RegionRecord

    @staticmethod
    def make(file_path: PosixPath) -> RegionTable:
        with open(file_path, "r") as f:
            return RegionTable(
                RegionSchema(many=True, unknown=RAISE).load(csv.DictReader(f))
            )
