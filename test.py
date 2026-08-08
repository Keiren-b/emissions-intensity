import duckdb
con = duckdb.connect("nem.duckdb")
con.sql("SELECT 42").show()
duckdb.sql("CALL start_ui();")