from __future__ import annotations
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from typing import Dict, List, NewType, Tuple
from typeguard import typechecked

from .primitives import Region

class KustoDataType(str, Enum):
    BOOL = "bool"
    DATETIME = "datetime"
    DYNAMIC = "dynamic"
    INT = "int"
    REAL = "real"
    STRING = "string"


KustoTableSchema = NewType("KustoTableSchema", List[Tuple[str, KustoDataType]])


@typechecked
class TableRow:
    def __init__(self, row_dict: Dict):
        for key in row_dict:
            setattr(self, key, row_dict[key])


@typechecked
class ClusterDatabase:
    def __init__(
        self,
        cluster_name: str,
        db_name: str,
        region: Region,
        dry_run: bool,
        uai_client_id: str = None,
    ):
        self.dry_run = dry_run
        self.cluster_name = cluster_name
        self.database_name = db_name
        if dry_run:
            self.client = None
            self.tables = []
        else:
            uri = f"https://{cluster_name}.{region.value.lower()}.kusto.windows.net"
            if uai_client_id is None:
                kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(uri)
            else:
                kcsb = KustoConnectionStringBuilder.with_aad_managed_service_identity_authentication(
                    uri, client_id=uai_client_id
                )
            self.client = KustoClient(kcsb)
            self.tables = self._get_current_tables()

    def get_table(self, name: str) -> Table:
        for table in self.tables:
            if table.name == name:
                return table
        raise RuntimeError(f"Unable to find table '{name}'.")

    def get_tables(self) -> List[Table]:
        return self.tables

    def _get_current_tables(self) -> List[Table]:
        tables = []
        for table in self.table_action_query(".show tables"):
            name = table["TableName"]
            result = self.table_action_query(f".show table {name} schema as json")[0]
            schema = KustoTableSchema(
                [
                    (col["Name"], KustoDataType(col["CslType"]))
                    for col in json.loads(result["Schema"])["OrderedColumns"]
                ]
            )
            tables.append(Table(self, result["TableName"], schema))
        return tables

    def _make_query_to_act_on_table(
        self, action: str, name: str, schema: KustoTableSchema
    ) -> str:
        table_query = f".{action} table {name} ("
        table_query += ",".join(
            [f"{col_name}: {col_datatype}" for (col_name, col_datatype) in schema]
        )
        return table_query + ")"

    def add_table(self, name: str, schema: KustoTableSchema):
        self.table_action_query(
            self._make_query_to_act_on_table("create", name, schema)
        )
        self.tables.append(Table(self, name, schema))
        logging.info(f"Created table '{name}'.")

    def add_or_update_table(self, name: str, schema: KustoTableSchema) -> Table:
        try:
            table = self.get_table(name)
            table.update(schema)
        except RuntimeError as ex:
            logging.warning(ex)
            self.add_table(name, schema)
        return self.get_table(name)

    def table_action_query(self, query: str):
        logging.info(f"Executing query: {query}")
        if not self.dry_run:
            result = self.client.execute(self.database_name, query)
            return result["Table_0"].to_dict()["data"]

    def row_action_query(self, query: str) -> List[TableRow]:
        logging.info(f"Executing query: {query}")
        if not self.dry_run:
            return [
                TableRow(row)
                for row in self.client.execute(self.database_name, query)
                .tables[1]
                .to_dict()["data"]
            ]

    def set_default_workload_group(self):
        if not self.dry_run:
            workload_group = json.loads(
                self.table_action_query(".show workload_group default")[0][
                    "WorkloadGroup"
                ]
            )

            # Only allow queries on hot cached data.
            workload_group["RequestLimitsPolicy"]["DataScope"]["IsRelaxable"] = False
            workload_group["RequestLimitsPolicy"]["DataScope"]["Value"] = "HotCache"
            self.table_action_query(
                f".create-or-alter workload_group default ```{json.dumps(workload_group)}```"
            )
        logging.info(f"Set default workload group.")


@typechecked
class Table:
    def __init__(self, adx: ClusterDatabase, name: str, schema: KustoTableSchema):
        self.adx = adx
        self.name = name
        self.schema = schema
        if self.adx.dry_run:
            self.mappings = []
            self.materialized_views = []
        else:
            self.mappings = self._get_current_mappings()
            self.materialized_views = self._get_current_mat_views()

    def _get_current_mappings(self) -> List[Mapping]:
        mappings = []
        for mapping in self.adx.table_action_query(
            f".show table {self.name} ingestion mappings"
        ):
            mappings.append(Mapping(self, mapping["Name"]))
        return mappings

    def _get_current_mat_views(self) -> List[MaterializedView]:
        return [
            MaterializedView(self, mv["Name"], mv["Query"], False)
            for mv in self.adx.table_action_query(f".show materialized-views")
            if mv["SourceTable"] == self.name
        ]

    def update(self, schema: KustoTableSchema):
        for col in schema:
            for curr_col in self.schema:
                if col[0] == curr_col[0] and col[1] != curr_col[1]:
                    self.adx.table_action_query(
                        f".alter column ['{self.name}'].['{col[0]}'] type={col[1]}"
                    )
        self.adx.table_action_query(
            self.adx._make_query_to_act_on_table("alter", self.name, schema)
        )
        logging.info(f"Updated table '{self.name}'.")

    def get_mapping(self, name: str):
        for mapping in self.mappings:
            if mapping.name == name:
                return mapping
        raise RuntimeError(f"Unable to find mapping '{name}'.")

    def add_mapping(self, name: str):
        query = f".create table {self.name} ingestion json mapping '{name}' '["
        query += ",".join(
            [
                f'{{"column": "{col}", "Properties": {{"Path": "$.{col}"}}}}'
                for (col, _) in self.schema
            ]
        )
        query += "]'"
        self.adx.table_action_query(query)
        self.mappings.append(Mapping(self, name))
        logging.info(f"Created mapping '{name}'.")

    def delete_mapping(self, name: str):
        self.adx.table_action_query(
            f'.drop table {self.name} ingestion json mapping "{name}"'
        )
        self.mappings = [m for m in self.mappings if m.name != name]
        logging.info(f"Deleted mapping '{name}'.")

    def add_or_recreate_mapping(self, name: str) -> Mapping:
        try:
            mapping = self.get_mapping(name)
            self.delete_mapping(name)
        except RuntimeError as ex:
            logging.warning(ex)
        self.add_mapping(name)
        return self.get_mapping(name)

    def get_materialized_view(self, name: str):
        for mv in self.materialized_views:
            if mv.name == name:
                return mv
        raise RuntimeError(f"Unable to find materialized view '{name}'.")

    def add_materialized_view(self, name: str, query: str):
        resp = self.adx.table_action_query(
            f".create async materialized-view with (backfill=true, effectiveDateTime=datetime({(datetime.today()-timedelta(days=14)).strftime('%Y-%m-%d')})) {name} on table {self.name} {{{query}}}"
        )
        self.materialized_views.append(MaterializedView(self, name, query, True))
        if self.adx.dry_run:
            msg = f"Asynchronously creating materialized view '{name}'."
        else:
            msg = f"Asynchronously creating materialized view '{name}' with operation ID '{resp[0]['OperationId']}'."
        logging.info(msg)

    def delete_materialized_view(self, name: str):
        self.adx.table_action_query(f".drop materialized-view {name}")
        self.materialized_views = [m for m in self.materialized_views if m.name != name]
        logging.info(f"Deleted materialized view '{name}'.")

    def add_or_update_materialized_view(
        self, name: str, query: str
    ) -> MaterializedView:
        try:
            mv = self.get_materialized_view(name)

            # Recreate modified materialized views. Only certain properties of a
            # materialized view may be updated using the `alter` command. Since views should
            # rarely be modified, recreate them instead to avoid complicated update logic.
            # Recreating view will cause temporary observability outage while new view is
            # computed. Observability outage may take several hours depending on the
            # materialized view's backfill date, table size, and query complexity.
            if mv.query != query:
                self.delete_materialized_view(name)
                self.add_materialized_view(name, query)
            else:
                mv.is_latest = True
                logging.info(f"Materialized view '{name}' unchanged.")
                # Only set retention policy for preexisting materialized views
                # since new views are created asynchronously.
                self.set_default_materialized_view_retention_policy(name)
        except RuntimeError as ex:
            logging.warning(ex)
            self.add_materialized_view(name, query)
            # Unable to add retention policy until view is created.
        return self.get_materialized_view(name)

    def delete_obsolete_materialized_views(self):
        for mv in self.materialized_views:
            if not mv.is_latest:
                self.delete_materialized_view(mv.name)

    def set_default_materialized_view_retention_policy(self, name: str):
        retention_policy = {
            "SoftDeletePeriod": "30.00:00:00",
            "Recoverability": "Disabled",
        }
        self.adx.table_action_query(
            f".alter materialized-view {name} policy retention ```{json.dumps(retention_policy)}```"
        )
        logging.info(f"Set default retention policy for materialized view '{name}'.")


@typechecked
class Mapping:
    def __init__(self, table: Table, name: str):
        self.table = table
        self.name = name


@typechecked
class MaterializedView:
    def __init__(self, table: Table, name: str, query: str, is_latest: bool):
        self.table = table
        self.name = name
        self.query = query
        self.is_latest = is_latest
