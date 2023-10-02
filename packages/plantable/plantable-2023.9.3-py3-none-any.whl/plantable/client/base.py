import asyncio
import logging
import time
from datetime import datetime, date
from typing import Callable, List, Union

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
import socketio
from fastapi import HTTPException, status
from pydantic import BaseModel
from pypika import MySQLQuery as PikaQuery
from pypika import Table as PikaTable
from pypika.dialects import QueryBuilder
from tabulate import tabulate
from ..serde.to_seatable import ToSeaTable
from ..model import (
    DTABLE_ICON_COLORS,
    DTABLE_ICON_LIST,
    Admin,
    ApiToken,
    Base,
    BaseActivity,
    BaseToken,
    Column,
    Metadata,
    SelectOption,
    Table,
    Team,
    User,
    UserInfo,
    View,
    Webhook,
)
from ..serde import ToPythonDict
from ..serde.column import SeaTableType
from .conf import SEATABLE_URL
from .core import TABULATE_CONF, HttpClient
from .exception import MoreRows

logger = logging.getLogger()

FIRST_COLUMN_TYPES = ["text", "number", "date", "single-select", "formular", "autonumber"]


################################################################
# Helpers
################################################################
# divide chunks
def divide_chunks(x: list, chunk_size: int):
    for i in range(0, len(x), chunk_size):
        yield x[i : i + chunk_size]


################################################################
# BaseClient
################################################################
class BaseClient(HttpClient):
    def __init__(
        self,
        seatable_url: str = SEATABLE_URL,
        api_token: str = None,
        base_token: BaseToken = None,
    ):
        super().__init__(seatable_url=seatable_url.rstrip("/"))

        self.base_token = base_token
        self.api_token = api_token

        if api_token:
            auth_url = self.seatable_url + "/api/v2.1/dtable/app-access-token/"
            response = requests.get(auth_url, headers={"Authorization": f"Token {self.api_token}"})
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as ex:
                error_msg = response.json()["error_msg"]
                if error_msg in ["Permission denied."]:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Wrong base token!",
                    )
                raise ex
            results = response.json()
            self.base_token = BaseToken(**results)

        self.dtable_uuid = self.base_token.dtable_uuid
        self.workspace_id = self.base_token.workspace_id
        self.group_id = self.base_token.group_id
        self.group_name = self.base_token.group_name
        self.base_name = self.base_token.base_name

    ################################################################
    # BASE INFO
    ################################################################
    # Get Base Info
    async def get_base_info(self):
        METHOD = "GET"
        URL = f"/dtable-server/dtables/{self.base_token.dtable_uuid}"

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL)

        return results

    # Get Metadata
    async def get_metadata(self, model: BaseModel = Metadata):
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/metadata/"
        ITEM = "metadata"

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL)
            results = response[ITEM]

        if model:
            results = model(**results)

        return results

    # (CUSTOM) List Tables
    async def list_tables(self):
        metadata = await self.get_metadata()
        tables = metadata.tables

        return tables

    # (CUSTOM) Get Table
    async def get_table(self, table_name: str):
        tables = await self.list_tables()
        for table in tables:
            if table.name == table_name:
                return table
        else:
            raise KeyError()

    # (CUSTOM) Get Table by ID
    async def get_table_by_id(self, table_id: str):
        tables = await self.list_tables()
        for table in tables:
            if table.id == table_id:
                return table
        else:
            raise KeyError()

    # (CUSTOM) Get Names by ID
    async def get_names_by_ids(self, table_id: str, view_id: str):
        table = await self.get_table_by_id(table_id=table_id)
        views = await self.list_views(table_name=table.name)
        for view in views:
            if view.id == view_id:
                break
        else:
            raise KeyError

        return table.name, view.name

    # Get Big Data Status
    async def get_bigdata_status(self):
        METHOD = "GET"
        URL = f"/dtable-db/api/v1/base-info/{self.base_token.dtable_uuid}/"

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL)

        return results

    # List Collaborators
    async def list_collaborators(self, model: BaseModel = UserInfo):
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/related-users/"
        ITEM = "user_list"

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL)
            results = response[ITEM]

        if model:
            results = [model(**x) for x in results]

        return results

    # (CUSTOM) ls
    async def ls(self, table_name: str = None):
        metadata = await self.get_metadata()
        tables = metadata.tables
        if table_name:
            for table in tables:
                if table.name == table_name:
                    break
            else:
                raise KeyError()
            columns = [{"key": c.key, "name": c.name, "type": c.type} for c in table.columns]
            print(tabulate(columns, **TABULATE_CONF))
            return
        _tables = list()
        for table in tables:
            _n = len(table.columns)
            _columns = ", ".join(c.name for c in table.columns)
            if len(_columns) > 50:
                _columns = _columns[:50] + "..."
            _columns += f" ({_n})"
            _tables += [
                {
                    "id": table.id,
                    "name": table.name,
                    "views": ", ".join([v.name for v in table.views]),
                    "columns": _columns,
                },
            ]
        print(tabulate(_tables, **TABULATE_CONF))

    ################################################################
    # ROWS
    ################################################################
    # List Rows (Table, with SQL)
    async def list_rows_with_sql(self, sql: Union[str, QueryBuilder], convert_keys: bool = True):
        """
        [NOTE]
         default LIMIT 100 when not LIMIT is given!
         max LIMIT 10000!
        """
        METHOD = "POST"
        URL = f"/dtable-db/api/v1/query/{self.base_token.dtable_uuid}/"

        json = {
            "sql": sql.get_sql() if isinstance(sql, QueryBuilder) else sql,
            "convert_keys": convert_keys,
        }
        SUCCESS = "success"
        ITEM = "results"

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, json=json)
            if not response[SUCCESS]:
                raise Exception(response)
            results = response[ITEM]

        return results

    # List Rows (View)
    # [NOTE] 4.1에서 첫 Row에 없는 값은 안 읽어오는 이슈
    async def list_rows(
        self,
        table_name: str,
        view_name: str,
        convert_link_id: bool = False,
        order_by: str = None,
        direction: str = "asc",
        start: int = 0,
        limit: int = None,
    ):
        MAX_LIMIT = 1000

        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/rows/"
        ITEM = "rows"

        get_all_rows = False
        if not limit:
            get_all_rows = True
            limit = limit or MAX_LIMIT

        params = {
            "table_name": table_name,
            "view_name": view_name,
            "convert_link_id": str(convert_link_id).lower(),
            "order_by": order_by,
            "direction": direction,
            "start": start,
            "limit": limit,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, **params)
            response = response[ITEM]
            results = response

            # pagination
            if get_all_rows:
                while len(response) == limit:
                    params.update({"start": params["start"] + limit})
                    response = await self.request(session=session, method=METHOD, url=URL, **params)
                    response = response[ITEM]
                    results += response

        return results

    # (CUSTOM) List Rows by ID
    async def list_rows_by_id(
        self,
        table_id: str,
        view_id: str,
        convert_link_id: bool = False,
        order_by: str = None,
        direction: str = "asc",
        start: int = 0,
        limit: int = None,
    ):
        table_name, view_name = self.get_names_by_ids(table_id=table_id, view_id=view_id)
        return await self.list_rows(
            table_name=table_name,
            view_name=view_name,
            convert_link_id=convert_link_id,
            order_by=order_by,
            direction=direction,
            start=start,
            limit=limit,
        )

    # Add Row
    async def add_row(
        self,
        table_name: str,
        row: dict,
        anchor_row_id: str = None,
        row_insert_position: str = "insert_below",
    ):
        # insert_below or insert_above
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/rows/"

        table = await self.get_table(table_name=table_name)
        serializer = ToSeaTable(table)

        json = {"table_name": table_name, "row": serializer(row)}
        if anchor_row_id:
            json.update(
                {
                    "ahchor_row_id": anchor_row_id,
                    "row_insert_position": row_insert_position,
                }
            )

        # add select options if not exists
        _ = await self.add_select_options_if_not_exists(table_name=table_name, rows=[row])

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Update Row
    async def update_row(self, table_name: str, row_id: str, row: dict):
        # NOT WORKING
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/rows/"
        ITEM = "success"

        table = await self.get_table(table_name=table_name)
        serializer = ToSeaTable(table=table)
        json = {"table_name": table_name, "row_id": row_id, "row": serializer(row)}

        # add select options if not exists
        _ = await self.add_select_options_if_not_exists(table_name=table_name, rows=[row])

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, json=json)
            results = response[ITEM]

        return results

    # Delete Row
    async def delete_row(self, table_name: str, row_id: str):
        METHOD = "DELETE"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/rows/"

        json = {"table_name": table_name, "row_id": row_id}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Get Row
    async def get_row(self, table_name: str, row_id: str, convert: bool = False):
        # NOT WORKING
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/rows/{row_id}/"

        params = {"table_name": table_name, "convert": str(convert).lower()}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, **params)

        return results

    # prep link columns
    @staticmethod
    def prep_link_columns(table: Table):
        return [c for c in table.columns if c.type == "link"]

    # Append Rows
    async def append_rows(self, table_name: str, rows: List[dict]):
        # insert_below or insert_above
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/batch-append-rows/"

        # get pk and serializer
        table = await self.get_table(table_name=table_name)
        serializer = ToSeaTable(table=table)

        # prep link columns
        link_columns = self.prep_link_columns(table=table)

        # add select options if not exists
        _ = await self.add_select_options_if_not_exists(table_name=table_name, rows=rows)

        # divide chunk - [NOTE] 1000 rows까지만 됨
        UPDATE_LIMIT = 1000
        chunks = divide_chunks(rows, UPDATE_LIMIT)
        list_json = [{"table_name": table_name, "rows": [serializer(r) for r in chunk]} for chunk in chunks]

        async with self.session_maker(token=self.base_token.access_token) as session:
            coros = [self.request(session=session, method=METHOD, url=URL, json=json) for json in list_json]
            list_results = await asyncio.gather(*coros)

        results = {"inserted_row_count": 0}
        for r in list_results:
            results["inserted_row_count"] += r["inserted_row_count"]

        # update link
        if link_columns:
            pass

        return results

    # Update Rows
    async def update_rows(self, table_name: str, updates: List[dict]):
        # updates = [{"row_id": xxx, "row": {"key": "value"}}, ...]
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/batch-update-rows/"

        # get serializer
        table = await self.get_table(table_name=table_name)
        serializer = ToSeaTable(table=table)

        # prep link columns
        link_columns = self.prep_link_columns(table=table)

        # add select options if not exists
        _ = await self.add_select_options_if_not_exists(
            table_name=table_name, rows=[update["row"] for update in updates]
        )

        # divide chunk - [NOTE] 1000 rows까지만 됨
        UPDATE_LIMIT = 1000
        chunks = divide_chunks(updates, UPDATE_LIMIT)
        list_json = [
            {
                "table_name": table_name,
                "updates": [{"row_id": r["row_id"], "row": serializer(r["row"])} for r in chunk],
            }
            for chunk in chunks
        ]

        async with self.session_maker(token=self.base_token.access_token) as session:
            coros = [self.request(session=session, method=METHOD, url=URL, json=json) for json in list_json]
            list_results = await asyncio.gather(*coros)

        results = None
        for r in list_results:
            if isinstance(r, Exception):
                raise r
            if not r["success"]:
                results = r
                break
        else:
            results = r

        return results

    # (CUSTOM) Upsert Rows
    async def upsert_rows(self, table_name: str, rows: List[dict], key_column: str = None):
        if not key_column:
            table = await self.get_table(table_name=table_name)
            key_column = table.columns[0].name

        row_id_map = await self.get_row_id_map(table_name=table_name, key_column=key_column)

        rows_to_update = list()
        rows_to_append = list()
        for row in rows:
            if row[key_column] in row_id_map:
                rows_to_update.append({"row_id": row_id_map[row[key_column]], "row": row})
            else:
                rows_to_append.append(row)

        results = dict()
        if rows_to_update:
            results_update = await self.update_rows(table_name=table_name, updates=rows_to_update)
            results.update({"update_rows": results_update})
        if rows_to_append:
            results_append = await self.append_rows(table_name=table_name, rows=rows_to_append)
            results.update({"append_rows": results_append})

        return results

    # Delete Rows
    async def delete_rows(self, table_name: str, row_ids: List[str]):
        METHOD = "DELETE"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/batch-delete-rows/"

        json = {"table_name": table_name, "row_ids": row_ids}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Rock Rows
    async def lock_rows(self, table_name: str, row_ids: List[str]):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/lock-rows/"

        json = {"table_name": table_name, "row_ids": row_ids}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Unrock Rows
    async def unlock_rows(self, table_name: str, row_ids: List[str]):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/unlock-rows/"

        json = {"table_name": table_name, "row_ids": row_ids}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    ################################################################
    # (CUSTOM) QUERY
    ################################################################
    # (CUSTOM) Query Key Map
    async def get_row_id_map(self, table_name: str, key_column: str = None):
        if key_column is None:
            table = await self.get_table(table_name=table_name)
            key_column = table.columns[0].name
        results = await self.read_table(table_name=table_name, columns=["_id", key_column])
        return {r[key_column]: r["_id"] for r in results}

    # (CUSTOM) read_table
    async def read_table(
        self,
        table_name: str,
        columns: List[str] = None,
        modified_before: str = None,
        modified_after: str = None,
        offset: int = 0,
        limit: int = None,
        mtime: str = "_mtime",
        deserialize: bool = True,
    ) -> List[dict]:
        MAX_LIMIT = 10000
        OFFSET = 0

        # correct args
        table = PikaTable(table_name)
        if not columns:
            columns = ["*"]
        if not isinstance(columns, list):
            columns = [x.strip() for x in columns.split(",")]
        _limit = min(MAX_LIMIT, limit) if limit else limit
        _offset = offset if offset else OFFSET

        q = PikaQuery.from_(table).select(*columns)
        if modified_before:
            if isinstance(modified_before, datetime):
                modified_before = modified_before.isoformat(timespec="milliseconds")
            q = q.where(table[mtime] < modified_before)
        if modified_after:
            if isinstance(modified_after, datetime):
                modified_after = modified_after.isoformat(timespec="milliseconds")
            q = q.where(table[mtime] > modified_after)
        q = q.limit(_limit or MAX_LIMIT)

        # 1st hit
        rows = await self.list_rows_with_sql(sql=q.offset(_offset))

        # get all records
        if not limit or len(rows) < limit:
            while True:
                _offset += MAX_LIMIT
                _rows = await self.list_rows_with_sql(sql=q.offset(_offset))
                rows += _rows
                if len(_rows) < MAX_LIMIT:
                    break

        # to python data type
        if deserialize:
            deserializer = await self.generate_deserializer(table_name=table_name)
            try:
                rows = [deserializer(r) for r in rows]
            except Exception as ex:
                _msg = (
                    f"deserializer failed - group '{self.group_name}', base '{self.base_name}', table '{table_name}'"
                )
                logger.error(_msg)
                raise ex

        return rows

    # (CUSTOM) read table as DataFrame
    async def read_table_as_df(
        self,
        table_name: str,
        columns: List[str] = None,
        modified_before: str = None,
        modified_after: str = None,
        offset: int = 0,
        limit: int = None,
        mtime: str = "_mtime",
        deserialize: bool = True,
    ):
        rows = await self.read_table(
            table_name=table_name,
            columns=columns,
            modified_before=modified_before,
            modified_after=modified_after,
            offset=offset,
            limit=limit,
            mtime=mtime,
            deserialize=deserialize,
        )

        if not rows:
            return None
        tbl = pa.Table.from_pylist(rows).to_pandas()
        return tbl.set_index("_id", drop=True).rename_axis("row_id")

    # (CUSTOM) read view
    async def read_view(
        self,
        table_name: str,
        view_name: str,
        convert_link_id: bool = False,
        order_by: str = None,
        direction: str = "asc",
        start: int = 0,
        limit: int = None,
        deserialize: bool = True,
    ):
        rows = await self.list_rows(
            table_name=table_name,
            view_name=view_name,
            convert_link_id=convert_link_id,
            order_by=order_by,
            direction=direction,
            start=start,
            limit=limit,
        )

        # to python data type
        if deserialize:
            deserializer = await self.generate_deserializer(table_name=table_name)
            try:
                rows = [deserializer(r) for r in rows]
            except Exception as ex:
                _msg = f"deserializer failed - group '{self.group_name}', base '{self.base_name}', table '{table_name}', view '{view_name}'"
                logger.error(_msg)
                raise ex

        return rows

    # (CUSTOM) read view as DataFrame
    async def read_view_as_df(
        self,
        table_name: str,
        view_name: str,
        convert_link_id: bool = False,
        order_by: str = None,
        direction: str = "asc",
        start: int = 0,
        limit: int = None,
        deserialize: bool = True,
    ):
        rows = await self.read_view(
            table_name=table_name,
            view_name=view_name,
            convert_link_id=convert_link_id,
            order_by=order_by,
            direction=direction,
            start=start,
            limit=limit,
            deserialize=deserialize,
        )

        if not rows:
            return None
        tbl = pa.Table.from_pylist(rows).to_pandas()
        return tbl.set_index("_id", drop=True).rename_axis("row_id")

    # (CUSTOM) Generate Deserializer
    async def generate_deserializer(self, table_name):
        table = await self.get_table(table_name)
        users = await self.list_collaborators() if "collaborator" in [c.type for c in table.columns] else None
        return ToPythonDict(table=table, users=users)

    ################################################################
    # LINKS
    ################################################################
    # Create Row Link
    # [NOTE] Not Working!
    async def create_row_link(
        self, table_name: str, table_row_id: str, other_table_name: str, other_table_row_id: str, link_id: str
    ):
        METHOD = "POST"
        URL = f"/dtable-db/api/v1/linked-records/{self.base_token.dtable_uuid}"

        json = {
            "table_id": table_name,
            "other_table_name": other_table_name,
            "link_id": link_id,
            "table_row_id": table_row_id,
            "other_table_row_id": other_table_row_id,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Create Row Links (1:n)
    async def create_row_links(
        self, table_name: str, other_table_name: str, link_id: str, row_id: str, other_rows_ids: List[str]
    ):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/links/"

        other_rows_ids = other_rows_ids if isinstance(other_rows_ids, list) else [other_rows_ids]

        json = {
            "table_name": table_name,
            "other_table_name": other_table_name,
            "link_id": link_id,
            "row_id": row_id,
            "other_rows_ids": other_rows_ids,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Create Row Links Batch (m:n)
    # [TBD]
    async def create_row_links_batch(
        self,
        table_name: str,
        other_table_name: str,
        link_id: str,
        row_id_list: List[str],
        other_rows_ids_map: List[str],
    ):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/batch-update-links/"

        table, other_table = await asyncio.gather(
            self.get_table(table_name=table_name), self.get_table(other_table_name=other_table_name)
        )

        json = {
            "table_id": table.id,
            "other_table_id": other_table.id,
            "link_id": link_id,
            "row_id_list": row_id_list,
            "other_rows_ids_map": other_rows_ids_map,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # List Row Links
    # [NOTE] Not Working!
    async def list_row_links(self, table_name: str, link_column: str, rows: list = None):
        METHOD = "POST"
        URL = f"/dtable-db/api/v1/linked-records/{self.base_token.dtable_uuid}"

        table = await self.get_table(table_name=table_name)

        json = {"table_id": table.id, "link_column": link_column, "rows": rows}

        print(json)

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # (custom) Get Link
    async def get_link(self, table_name: str, column_name: str):
        column = await self.get_column(table_name=table_name, column_name=column_name)
        if column.type != "link":
            _msg = f"type of column '{column_name}' is not link type."
            raise KeyError(_msg)
        return column.data

    # (custom) Get Ohter Rows Ids
    async def get_other_rows_ids(self, table_name, column_name):
        link = await self.get_link(table_name=table_name, column_name=column_name)
        other_table = await self.get_table_by_id(table_id=link["other_table_id"])
        for column in other_table.columns:
            if column.key == link["display_column_key"]:
                break
        else:
            raise KeyError
        return await self.get_row_id_map(table_name=other_table.name, key_column=column.name)

    # (custom)
    async def upsert_link_rows(self, table: Table, column_name: str, rows: List[dict], key_column: str = None):
        map_pk_to_row_id = await self.get_row_id_map(table.name, key_column=key_column)
        pass
        # [HERE!!!]

    ################################################################
    # FILES & IMAGES
    ################################################################

    ################################################################
    # TABLES
    ################################################################
    # Add Table
    async def add_table(self, table_name: str):
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/tables/"

        json = {"table_name": table_name}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Create New Table
    # [NOTE] 이 endpoint는 Link 컬럼을 처리하지 못 함. (2023.9.9 현재)
    async def create_new_table(self, table_name: str, columns: List[Union[dict, SeaTableType]]):
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/tables/"

        json = {
            "table_name": table_name,
            "columns": [c.seatable_schema() if isinstance(c, SeaTableType) else c for c in columns]
            if columns
            else None,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # (custom) Create Table
    # [NOTE] 현재 Create New Table API 문제 때문에 사용 - 2번째 Colmnn부터는 insert_column으로 추가.
    async def create_table(self, table_name: str, columns: List[Union[dict, SeaTableType]], exist_ok: bool = True):
        # check if already exists
        tables = await self.list_tables()
        if table_name in tables:
            if not exist_ok:
                _msg = f"table '{table_name}' already exists!"
                raise KeyError(_msg)
            return

        # parse column type
        columns = [c.seatable_schema() if isinstance(c, SeaTableType) else c for c in columns]

        # seprate key column
        key_column, columns = columns[0], columns[1:]
        if key_column["column_type"] not in FIRST_COLUMN_TYPES:
            _msg = f"""only '{", ".join(FIRST_COLUMN_TYPES)}' can be a first column"""
            raise KeyError(_msg)

        # create table
        _ = await self.create_new_table(table_name=table_name, columns=[key_column])

        # insert columns
        for column in columns:
            _ = await self.insert_column(table_name=table_name, column=column)
        return

    # Rename Table
    async def rename_table(self, table_name: str, new_table_name: str):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/tables/"

        json = {"table_name": table_name, "new_table_name": new_table_name}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Delete Table
    async def delete_table(self, table_name: str):
        METHOD = "DELETE"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/tables/"

        json = {"table_name": table_name}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Duplicate Table
    async def duplicate_table(self, table_name: str, is_duplicate_records: bool = True):
        # rename table in a second step
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/tables/duplicate-table/"

        json = {"table_name": table_name, "is_duplicate_records": is_duplicate_records}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    ################################################################
    # IMPORT
    ################################################################
    # (DEPRECATED) Create Table from CSV

    # (DEPRECATED) Append Rows from CSV

    ################################################################
    # VIEWS
    ################################################################
    # List Views
    async def list_views(self, table_name: str, model: BaseModel = View):
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/views/"
        ITEM = "views"

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, table_name=table_name)
            results = response[ITEM]

        if model:
            results = [model(**x) for x in results]

        return results

    # Create View
    async def create_view(
        self,
        table_name: str,
        name: str,
        type: str = "table",
        is_locked: bool = False,
        model: BaseModel = View,
    ):
        """
        type: "table" or "archive" (bigdata)
        """
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/views/"

        json = {
            "name": name,
            "type": type,
            "is_locked": str(is_locked).lower(),
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(
                session=session,
                method=METHOD,
                url=URL,
                json=json,
                table_name=table_name,
            )

        if model:
            results = model(**results)

        return results

    # Get View
    async def get_view(self, table_name: str, view_name: str, model: BaseModel = View):
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/views/{view_name}/"

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, table_name=table_name)

        if model:
            results = model(**results)

        return results

    # (CUSTOM) Get View by ID
    async def get_view_by_id(self, table_id: str, view_id: str, model: BaseModel = View):
        table_name, view_name = await self.get_names_by_ids(table_id=table_id, view_id=view_id)

        return await self.get_view(table_name=table_name, view_name=view_name)

    # Update View
    # NOT TESTED!
    async def update_view(self, table_name: str, view_name: str, conf: Union[dict, BaseModel] = None):
        METHOD = "PUT"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/views/{view_name}/"

        if isinstance(conf, BaseModel):
            conf = conf.dict()

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(
                session=session,
                method=METHOD,
                url=URL,
                json=conf,
                table_name=table_name,
            )

        return results

    # Delete View
    async def delete_view(self, table_name: str, view_name: str):
        METHOD = "DELETE"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/views/{view_name}/"
        ITEM = "success"

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, table_name=table_name)
            results = response[ITEM]

        return results

    ################################################################
    # COLUMNS
    ################################################################
    # Insert Column
    async def insert_column(self, table_name: str, column: Union[dict, SeaTableType]):
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/columns/"

        column = column.seatable_schema() if isinstance(column, SeaTableType) else column
        json = {"table_name": table_name, **column}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # Append Columns
    # [NOTE] 이 endpoint는 Link 컬럼을 처리하지 못 함. (2023.9.9 현재)
    async def append_columns(self, table_name: str, columns: List[Union[dict, SeaTableType]]):
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/batch-append-columns/"

        json = {
            "table_name": table_name,
            "columns": [c.seatable_schema() if isinstance(c, SeaTableType) else c for c in columns]
            if columns
            else None,
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        return results

    # (custom) Get Column
    async def get_column(self, table_name: str, column_name: str):
        table = await self.get_table(table_name=table_name)
        for column in table.columns:
            if column.name == column_name:
                return column
        else:
            _msg = f"no column (name: {column_name}) in table (name: {table_name})."
            raise KeyError(_msg)

    # (custom) Get Column by ID
    async def get_column_by_id(self, table_id: str, column_id: str):
        table = await self.get_table_by_id(table_id=table_id)
        for column in table.columns:
            if column.key == column_id:
                return column
        else:
            _msg = f"no column (id: {column_id}) in table (id: {table_id})."
            raise KeyError(_msg)

    # Add Select Options
    async def add_select_options(
        self, table_name: str, column_name: str, options: List[SelectOption], model: BaseModel = None
    ):
        METHOD = "POST"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/column-options/"

        json = {
            "table_name": table_name,
            "column": column_name,
            "options": [opt.dict(exclude_none=True) for opt in options],
        }

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, json=json)

        if model:
            results = model(**results)

        return results

    # (custom) add select options if not exists
    async def add_select_options_if_not_exists(self, table_name: str, rows: List[dict]):
        table = await self.get_table(table_name=table_name)
        columns_and_options = {
            c.name: [o["name"] for o in c.data["options"]] if c.data else []
            for c in table.columns
            if c.type in ["single-select", "multiple-select"]
        }

        if not columns_and_options:
            return

        options = {c: set([r.get(c) for r in rows if r.get(c)]) for c in columns_and_options}
        options_to_add = dict()
        for column_name, column_options in options.items():
            for column_opt in column_options:
                if column_opt not in columns_and_options[column_name]:
                    if column_name not in options_to_add:
                        options_to_add[column_name] = list()
                    options_to_add[column_name].append(SelectOption(name=column_opt))

        coros = [
            self.add_select_options(table_name=table_name, column_name=column_name, options=options)
            for column_name, options in options_to_add.items()
        ]

        return await asyncio.gather(*coros)

    ################################################################
    # BIG DATA
    ################################################################

    ################################################################
    # ROW COMMENTS
    ################################################################
    async def list_row_comments(self, row_id: str):
        # NOT WORKING
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/comments/"

        params = {"row_id": row_id}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, **params)

        return results

    ################################################################
    # NOTIFICATION
    ################################################################

    ################################################################
    # ACTIVITIES & LOGS
    ################################################################
    # Get Base Activity Logs
    async def get_base_activity_log(self, page: int = 1, per_page: int = 25, model: BaseModel = BaseActivity):
        # rename table in a second step
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/operations/"
        ITEM = "operations"

        params = {"page": page, "per_page": per_page}

        async with self.session_maker(token=self.base_token.access_token) as session:
            response = await self.request(session=session, method=METHOD, url=URL, **params)
            results = response[ITEM]

        if model:
            results = [model(**x) for x in results]

        return results

    # List Row Activities
    async def list_row_activities(self, row_id: str, page: int = 1, per_page: int = 25):
        # rename table in a second step
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/activities/"

        params = {"row_id": row_id, "page": page, "per_page": per_page}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, **params)

        return results

    # List Delete Operation Logs
    async def list_delete_operation_logs(self, op_type: str, page: int = 1, per_page: int = 25):
        """
        op_type
         delete_row
         delete_rows
         delete_table
         delete_column
        """
        # rename table in a second step
        METHOD = "GET"
        URL = f"/api/v2.1/dtables/{self.base_token.dtable_uuid}/delete-operation-logs/"

        params = {"op_type": op_type, "page": page, "per_page": per_page}

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL, **params)

        return results

    # List Delete Rows
    async def list_delete_rows(self):
        # rename table in a second step
        METHOD = "GET"
        URL = f"/dtable-server/api/v1/dtables/{self.base_token.dtable_uuid}/deleted-rows/"

        async with self.session_maker(token=self.base_token.access_token) as session:
            results = await self.request(session=session, method=METHOD, url=URL)

        return results

    ################################################################
    # SNAPSHOTS
    ################################################################
    # TBD
