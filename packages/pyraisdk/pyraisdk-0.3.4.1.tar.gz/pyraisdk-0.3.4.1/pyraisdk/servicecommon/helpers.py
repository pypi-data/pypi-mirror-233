from __future__ import annotations
from enum import Enum
import json
from pathlib import Path, PosixPath
from random import randint, randrange
from tempfile import gettempdir
from typeguard import typechecked
from typing import Dict

from .processtools import CommandOutcome, run

@typechecked
class Serializable:
    def to_dict(self) -> Dict:
        result = {}
        for (k, v) in self.__dict__.items():
            if type(v) in [list, set]:
                result[k] = [
                    elem.to_dict() if isinstance(elem, Serializable) else elem
                    for elem in v
                ]
            elif isinstance(v, Serializable):
                result[k] = v.to_dict()
            elif isinstance(v, Enum):
                result[k] = v.value
            elif v is not None:
                result[k] = v
        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

@typechecked
class DeploymentOutcome:
    @staticmethod
    def invoke_grpc_orchestrator(
        host_name: str,
        dep_name: str,
        token: str,
        orch_repo_root_path: Path,
        dry_run: bool = False,
    ) -> CommandOutcome:
        cmd = f"""
                {orch_repo_root_path.joinpath("raicli")} \
                -host '{host_name}' \
                -policyid 201 -stream-completion=true -stream-prompt=true -token {token} \
                -headers=azureml-model-deployment,{dep_name}       
                """
        return run(
            " ".join(cmd.split()), throw_on_error=False, retries=3, dry_run=dry_run
        )

    @staticmethod
    def invoke_http_model_endpoint(
        base_url: str,
        dep_name: str,
        corr_id_prefix: str,
        sample_post_data: str,
        token: str,
        dry_run: bool = False,
    ) -> CommandOutcome:
        cmd = f"""
                curl --verbose -w '%{{http_code}}'
                -H 'Content-Type: application/json'
                -H 'azureml-model-deployment: {dep_name}'
                -H 'Correlation-Id:{corr_id_prefix+str(randrange(10**7,10**8))}'
                -H 'Element: 0'
                -H 'Authorization: Bearer {token}'
                '{base_url}'
                -d '{sample_post_data}'
                """
        return run(
            " ".join(cmd.split()), throw_on_error=False, retries=3, dry_run=dry_run
        )

@typechecked
def make_temp_file_name() -> PosixPath:
    return Path(gettempdir()).joinpath(f"{randint(10**(8-1), (10**8)-1)}.xyz")
