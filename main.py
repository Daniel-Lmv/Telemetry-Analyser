import duckdb

# Caminho para o arquivo gerado pelo LMU
con = duckdb.connect(
    r"C:\Program Files (x86)\Steam\steamapps\common\Le Mans Ultimate\UserData\Telemetry\Autodromo Nazionale Monza_P_2026-07-07T23_43_42Z.duckdb",
    read_only=True,
)

# Lista todas as tabelas
tables = con.execute("SHOW TABLES").fetchall()
print(tables, "\n")
