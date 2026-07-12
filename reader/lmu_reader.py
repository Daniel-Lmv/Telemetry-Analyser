from pathlib import Path
from typing import Any

import duckdb
from pandas import DataFrame

from domain.session import ChannelInfo, EventInfo, Session
from reader.telemetry_reader import TelemetryReader


class LMUReader(TelemetryReader):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._connection: duckdb.DuckDBPyConnection | None = None

    @property
    def con(self) -> duckdb.DuckDBPyConnection:
        if self._connection is None:
            raise RuntimeError("Connection is not open.")
        return self._connection

    def load(self) -> Session:
        try:
            self._connect()
            return Session(
                metadata=self._read_metadata(),
                channel_info=self._read_channel_info(),
                channel_data=self._read_channel_data(),
                event_info=self._read_event_info(),
                event_data=self._read_event_data(),
            )

        finally:
            self._disconnect()

    def _connect(self) -> None:
        self._connection = duckdb.connect(str(self.file_path), read_only=True)

    def _disconnect(self) -> None:
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _read_metadata(self) -> dict[str, Any]:
        df = self._query_df('SELECT key, value FROM "metadata"')
        return dict(zip(df["key"], df["value"]))

    def _read_channel_info(self) -> dict[str, ChannelInfo]:
        rows = self._query_rows(
            'SELECT channelName, frequency, unit FROM "channelsList"'
        )
        return {
            channel_name: ChannelInfo(
                frequency=frequency,
                unit=unit,
            )
            for channel_name, frequency, unit in rows
        }

    def _read_channel_data(self) -> dict[str, DataFrame]:
        return self._read_tables("channelsList", "channelName")

    def _read_event_info(self) -> dict[str, EventInfo]:
        rows = self._query_rows("SELECT eventName, unit FROM eventsList")
        return {event_name: EventInfo(unit=unit) for event_name, unit in rows}

    def _read_event_data(self) -> dict[str, DataFrame]:
        return self._read_tables("eventsList", "eventName")

    def _read_tables(self, source_table: str, column_name: str) -> dict[str, DataFrame]:
        data: dict[str, DataFrame] = {}

        sources = self._query_df(f'SELECT "{column_name}" FROM "{source_table}"')
        for source_name in sources[column_name]:
            data[source_name] = self._query_df(f'SELECT * FROM "{source_name}"')
        return data

    def _query_df(self, sql: str) -> DataFrame:
        return self.con.execute(sql).fetchdf()

    def _query_rows(self, sql: str) -> list[tuple]:
        return self.con.execute(sql).fetchall()
