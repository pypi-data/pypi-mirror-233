from __future__ import annotations
from pathlib import Path, PosixPath
import shutil
from typeguard import typechecked
from typing import Any, Dict
from uuid import UUID

from .helpers import *
from .primitives import Region
from .processtools import CommandOutcome, run


# Deployment
@typechecked
class DeploymentGroup:
    def __init__(self, dep: Deployment, rg: str):
        self.dep = dep
        self.rg = rg

    def create(
        self,
        arm_template_path: Path,
        param_map: Dict[str, Any],
        throw_on_error: bool = True,
    ) -> CommandOutcome:
        # Copy ARM template to temporary file to avoid collisions while deploying
        # resources from ARM templates with the same name.
        temp_arm_template_path = make_temp_file_name()
        shutil.copy2(arm_template_path, temp_arm_template_path)
        cmd = f"""
            az deployment group create 
            --mode incremental 
            --resource-group {self.rg}
            --template-file {temp_arm_template_path}
            --parameters {' '.join([f"{k}={v}" for (k, v) in param_map.items()])}
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.dep.az.dry_run,
        )


@typechecked
class Deployment:
    def __init__(self, az: Az):
        self.az = az

    def group(self, rg: str) -> DeploymentGroup:
        return DeploymentGroup(self, rg)


# Resource group
@typechecked
class Group:
    def __init__(self, az: Az, name: str):
        self.az = az
        self.name = name

    def create(self, location: Region):
        run(
            f"az group create --location {location.name.lower()} --name {self.name}",
            dry_run=self.az.dry_run,
        )


# Key Vault
@typechecked
class Secret:
    def __init__(self, kv: KeyVault, name: str):
        self.kv = kv
        self.name = name

    def show(self) -> CommandOutcome:
        # Attempt to use cached secret value.
        if self.kv.secrets.get(self.name) is not None:
            return self.kv.secrets.get(self.name)
        outcome = run(
            f"az keyvault secret show --vault-name {self.kv.name} --name {self.name}",
            dry_run=self.kv.az.dry_run,
        )
        self.kv.secrets[self.name] = outcome
        return outcome


@typechecked
class KeyVault:
    def __init__(self, az: Az, rg: str, name: str):
        self.az = az
        self.rg = rg
        self.name = name
        self.secrets = {}

    def secret(self, name: str) -> Secret:
        return Secret(self, name)


# Resource
@typechecked
class Resource:
    def __init__(self, az: Az, sub: UUID, rg: str):
        self.az = az
        self.sub = sub
        self.rg = rg

    def show(
        self, name: str, resource_type: str, throw_on_error: bool = True
    ) -> CommandOutcome:
        cmd = f"""
            az resource show
            --subscription {self.sub}
            --resource-group {self.rg}
            --name {name}
            --resource-type {resource_type}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.az.dry_run,
        )


# Machine Learning
@typechecked
class AmlDeployment:
    def __init__(self, ml: Aml, ep: str):
        self.ml = ml
        self.ep = ep

    # WARNING: "az ml online-deployment delete" method in az
    # ml CLI version 2.11.0 does not raise any indication of an
    # error if parameter names are invalid.
    def delete(self, name: str, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-deployment delete
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --endpoint-name {self.ep}
            --name {name}
            --yes
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.ml.az.dry_run,
        )

    def get_logs(self, name: str) -> CommandOutcome:
        cmd = f"""
            az ml online-deployment get-logs
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --endpoint-name {self.ep}
            --name {name}
            --lines 10000
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.ml.az.dry_run,
        )

    def list(self, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-deployment list
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --endpoint-name {self.ep}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.ml.az.dry_run,
            throw_on_error=throw_on_error,
        )

    def show(self, name: str, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-deployment show
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --endpoint-name {self.ep}
            --name {name}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.ml.az.dry_run,
        )

    def update(self, name: str, set_arg: str):
        cmd = f"""
            az ml online-deployment update
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --endpoint-name {self.ep}
            --name {name}
            --set {set_arg}
            --only-show-errors
        """
        run(" ".join(cmd.split()), dry_run=self.ml.az.dry_run)


@typechecked
class AmlEndpoint:
    def __init__(self, ml: Aml):
        self.ml = ml

    def delete(self, name: str, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-endpoint delete
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --name {name}
            --yes
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.ml.az.dry_run,
        )

    def get_credentials(
        self, name: str, throw_on_error: bool = True, retries: int = 1
    ) -> CommandOutcome:
        cmd = f"""
            az ml online-endpoint get-credentials
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --name {name}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.ml.az.dry_run,
            throw_on_error=throw_on_error,
            retries=retries,
        )

    def list(self, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-endpoint list
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.ml.az.dry_run,
            throw_on_error=throw_on_error,
        )

    def show(self, name: str, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az ml online-endpoint show
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --name {name}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.ml.az.dry_run,
        )

    def update(self, name: str, set_arg: str):
        cmd = f"""
            az ml online-endpoint update
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --name {name}
            --set {set_arg}
            --only-show-errors
        """
        run(" ".join(cmd.split()), dry_run=self.ml.az.dry_run)

    def update_traffic(
        self,
        name: str,
        live_traffic_dist: Dict[str, int] = {},
        mirror_traffic_dist: Dict[str, int] = {},
    ):
        # Mirror traffic cannot be set unless live traffic is already set.
        if live_traffic_dist == {} and mirror_traffic_dist == {}:
            return
        cmd = f"""
            az ml online-endpoint update
            --resource-group {self.ml.rg}
            --workspace {self.ml.ws}
            --name {name}
        """
        if live_traffic_dist != {}:
            cmd += f" --traffic '{' '.join([f'{k}={v}' for (k, v) in live_traffic_dist.items()])}'"
        if mirror_traffic_dist != {}:
            cmd += f" --mirror-traffic '{' '.join([f'{k}={v}' for (k, v) in mirror_traffic_dist.items()])}'"
        cmd += " --only-show-errors"
        run(" ".join(cmd.split()), dry_run=self.ml.az.dry_run)


@typechecked
class Aml:
    def __init__(self, az: Az, rg: str, ws: str):
        self.az = az
        self.rg = rg
        self.ws = ws

    def deployment(self, ep: str) -> AmlDeployment:
        return AmlDeployment(self, ep)

    def endpoint(self) -> AmlEndpoint:
        return AmlEndpoint(self)


# Storage
@typechecked
class Directory:
    def __init__(self, sa_blob: StorageBlob, path: str):
        self.sa_blob = sa_blob
        self.path = path

    def list(self, throw_on_error: bool = False) -> CommandOutcome:
        cmd = f"""
            az storage blob directory list
            --account-name {self.sa_blob.sa}
            --container-name {self.sa_blob.container}
            --directory-path {self.path}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            throw_on_error=throw_on_error,
            dry_run=self.sa_blob.az.dry_run,
        )


@typechecked
class Metadata:
    def __init__(self, sa_blob: StorageBlob, blob_path: str):
        self.sa_blob = sa_blob
        self.blob_path = blob_path

    def update(self, metadata_map: Dict[str, str]):
        cmd = f"""
            az storage blob metadata update
            --account-name {self.sa_blob.sa}
            --container-name {self.sa_blob.container}
            --name {self.blob_path}
            --auth-mode login
            --metadata '{' '.join([f"{k}={v}" for (k, v) in metadata_map.items()])}'
            --only-show-errors
        """
        run(" ".join(cmd.split()), dry_run=self.sa_blob.az.dry_run)


@typechecked
class StorageBlob:
    def __init__(self, az: Az, sa: str, container: str):
        self.az = az
        self.sa = sa
        self.container = container

    def directory(self, path: str) -> Directory:
        return Directory(self, path)

    def download(self, name: str, output_path: PosixPath, sa_sas: str = None):
        cmd = f"""
            az storage blob download
            --account-name {self.sa}
            --container-name {self.container}
            --name {name}
            --file {output_path}
            --only-show-errors
        """
        if sa_sas is not None:
            cmd += f"--sas-token {sa_sas}"
        run(
            " ".join(cmd.split()), timeout_sec=600, dry_run=self.az.dry_run
        )

    def upload(self, name: str, input_path: str):
        cmd = f"""
            az storage blob upload
            --account-name {self.sa}
            --container-name {self.container}
            --name {name}
            --file {input_path}
            --overwrite
            --only-show-errors
        """
        run(" ".join(cmd.split()), dry_run=self.az.dry_run)

    def metadata(self, blob_path: str) -> Metadata:
        return Metadata(self, blob_path)


@typechecked
class CosmosDB:
    def __init__(self, az: Az, sub: UUID, rg: str, name: str):
        self.az = az
        self.sub = sub
        self.rg = rg
        self.name = name

    def list_keys(self) -> CommandOutcome:
        cmd = f"""
            az cosmosdb keys list
            --subscription {self.sub}
            --resource-group {self.rg}
            --name {self.name}
            --only-show-errors
        """
        return run(" ".join(cmd.split()), dry_run=self.az.dry_run)


# Azure Container Registry
@typechecked
class Manifest:
    def __init__(self, cr: ContainerRegistry, cr_name: str, image: str):
        self.cr = cr
        self.cr_name = cr_name
        self.image = image

    def show(self) -> CommandOutcome:
        cmd = (
            f"az acr manifest show -r {self.cr_name} -n {self.image} --only-show-errors"
        )
        return run(cmd, throw_on_error=False, dry_run=self.cr.az.dry_run)


@typechecked
class Credential:
    def __init__(self, cr: ContainerRegistry, cr_name: str):
        self.cr = cr
        self.cr_name = cr_name

    def show(self) -> CommandOutcome:
        cmd = f"az acr credential show --subscription {self.cr.sub} --resource-group {self.cr.rg} --name {self.cr_name} --only-show-errors"
        return run(cmd, dry_run=self.cr.az.dry_run)


@typechecked
class ContainerRegistry:
    def __init__(self, az: Az, sub: UUID, rg: str):
        self.az = az
        self.sub = sub
        self.rg = rg

    def manifest(self, name: str, image: str) -> Manifest:
        return Manifest(self, name, image)

    def login(self, name: str):
        cmd = f"az acr login --name {name} --only-show-errors"
        run(cmd, dry_run=self.az.dry_run)

    def credential(self, name: str) -> Credential:
        return Credential(self, name)

    def import_image(
        self, name: str, source: str, image: str, username: str, password: str
    ):
        cmd = f"az acr import --name {name} --source {source} --image {image} --username {username} --password {password}"
        run(cmd, dry_run=self.az.dry_run)


# Azure Account
@typechecked
class Subscription:
    def __init__(self, account: Account):
        self.account = account

    def list(self) -> CommandOutcome:
        cmd = f"""
            az account subscription list
            --only-show-errors
        """
        return run(" ".join(cmd.split()), dry_run=self.account.az.dry_run)


@typechecked
class Account:
    def __init__(self, az: Az):
        self.az = az

    def get_access_token(
        self, resource: str, throw_on_error: bool = True, retries: int = 1
    ) -> CommandOutcome:
        cmd = f"""
            az account get-access-token
            --resource {resource}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.az.dry_run,
            throw_on_error=throw_on_error,
            retries=retries,
        )

    def set(self, sub: UUID, throw_on_error: bool = True) -> CommandOutcome:
        cmd = f"""
            az account set
            --subscription {sub}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()),
            dry_run=self.az.dry_run,
            throw_on_error=throw_on_error,
        )

    def subscription(self) -> Subscription:
        return Subscription(self)


# Azure Container Instances
@typechecked
class Container:
    def __init__(self, az: Az, rg: str):
        self.az = az
        self.rg = rg

    def show(self, name: str) -> CommandOutcome:
        cmd = f"az container show --resource-group {self.rg} --name {name} --only-show-errors"
        return run(
            " ".join(cmd.split()), throw_on_error=False, dry_run=self.az.dry_run
        )

    def delete(self, name: str) -> CommandOutcome:
        cmd = f"az container delete --resource-group {self.rg} --name {name} --yes --only-show-errors"
        return run(
            " ".join(cmd.split()), throw_on_error=False, dry_run=self.az.dry_run
        )

    def list(self) -> CommandOutcome:
        cmd = f"az container list --resource-group {self.rg} --only-show-errors"
        return run(
            " ".join(cmd.split()), throw_on_error=False, dry_run=self.az.dry_run
        )


# Azure
@typechecked
class Az:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def account(self) -> Account:
        return Account(self)

    def acr(self, sub: UUID, rg: str) -> ContainerRegistry:
        return ContainerRegistry(self, sub, rg)

    def container(self, rg: str) -> Container:
        return Container(self, rg)

    def deployment(self) -> Deployment:
        return Deployment(self)

    def group(self, rg: str) -> Group:
        return Group(self, rg)

    def keyvault(self, rg: str, name: str) -> KeyVault:
        return KeyVault(self, rg, name)

    def login(
        self, identity_resource_id: str, throw_on_error: bool = True
    ) -> CommandOutcome:
        cmd = f"""
            az login
            --identity
            --username {identity_resource_id}
            --only-show-errors
        """
        return run(
            " ".join(cmd.split()), dry_run=self.dry_run, throw_on_error=throw_on_error
        )

    def ml(self, rg: str, ws: str) -> Aml:
        return Aml(self, rg, ws)

    def resource(self, sub: UUID, rg: str) -> Resource:
        return Resource(self, sub, rg)

    def rest_get(self, url: str) -> CommandOutcome:
        cmd = f"az rest --method get --url {url} --only-show-errors"
        return run(cmd, dry_run=self.dry_run)

    def storage_blob(self, sa: str, container: str) -> StorageBlob:
        return StorageBlob(self, sa, container)

    def cosmos_db(self, sub: UUID, rg: str, name: str) -> CosmosDB:
        return CosmosDB(self, sub, rg, name)


@typechecked
class AzCopy:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def copy(
        self,
        source_sa: str,
        source_full_path: str,
        target_sa: str,
        target_full_path: str,
        throw_on_error: bool,
        source_sa_sas: str = None,
        target_sa_sas: str = None,
    ) -> CommandOutcome:
        source_url = f"https://{source_sa}.blob.core.windows.net/{source_full_path}"
        if source_sa_sas is not None:
            source_url += f"?{source_sa_sas}"
        target_url = f"https://{target_sa}.blob.core.windows.net/{target_full_path}"
        if target_sa_sas is not None:
            target_url += f"?{target_sa_sas}"
        cmd = f"azcopy cp '{source_url}' '{target_url}'"
        return run(
            " ".join(cmd.split()), throw_on_error=throw_on_error, dry_run=self.dry_run
        )

    def login(self, identity_resource_id: str):
        cmd = f"""
            azcopy login
            --identity
            --identity-resource-id {identity_resource_id}
        """
        run(" ".join(cmd.split()), dry_run=self.dry_run)


@typechecked
class Docker:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def images(self, filter: str = None, format: str = None) -> CommandOutcome:
        cmd = "docker images"
        if filter != None:
            cmd += f" --filter={filter}"
        if format != None:
            cmd += f" --format {format}"
        return run(cmd, throw_on_error=False, dry_run=self.dry_run)

    def login(self, server_uri: str, username: str = None, password: str = None):
        cmd = f"docker login {server_uri}"
        if username is not None or password is not None:
            assert (
                username is not None and password is not None
            ), "Username and password must be passed together."
            cmd += f" --username {username} --password {password}"
        run(cmd, dry_run=self.dry_run)

    def pull(self, image_uri: str):
        run(f"docker pull {image_uri}", dry_run=self.dry_run)

    def push(self, image_uri: str):
        run(f"docker push {image_uri}", dry_run=self.dry_run)

    def tag(self, source_image_uri: str, target_image_uri: str):
        run(
            f"docker tag {source_image_uri} {target_image_uri}", dry_run=self.dry_run
        )
