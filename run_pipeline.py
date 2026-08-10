import duckdb
import pathlib

con = duckdb.connect("nem.duckdb")

for sql_file in sorted(pathlib.Path("sql").glob("*.sql")):
    print("Running", sql_file.name)
    con.execute(sql_file.read_text())

print("Pipeline complete.")