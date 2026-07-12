from pathlib import Path

from mapper.lmu_mapper import LMUMapper
from reader.lmu_reader import LMUReader

path = Path(
    "C:/Program Files (x86)/Steam/steamapps/common/Le Mans Ultimate/UserData/Telemetry/Autodromo Nazionale Monza_P_2026-07-07T23_43_42Z.duckdb"
)

reader = LMUReader(path)
session = reader.load()

mapper = LMUMapper()
mapped = mapper.map(session)

print(mapped.metadata)
print("\n", mapped.signals)
