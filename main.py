from pathlib import Path

import pandas as pd

from mapper.lmu_mapper import LMUMapper
from pipeline.telemetry_pipeline import TelemetryPipeline
from reader.lmu_reader import LMUReader
from transform.synchronizer import Synchronizer
from transform.telemetry_builder import TelemetryBuilder
from transform.telemetry_session_builder import TelemetrySessionBuilder

path = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Le Mans Ultimate\UserData\Telemetry\Sebring International Raceway_R_2026-07-19T20_28_44Z.duckdb"
)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

reader = LMUReader(Path(path))
session = reader.load()

pipeline = TelemetryPipeline(
    mapper=LMUMapper(),
    synchronizer=Synchronizer(),
    builder=TelemetryBuilder(),
    telemetry_session_builder=TelemetrySessionBuilder(),
)

telemetry_session = pipeline.run(session)
telemetry_session.telemetry.data.to_csv("head.csv", index=True)
