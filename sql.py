import duckdb
con = duckdb.connect("nem.duckdb")

con.sql("""
    SELECT * FROM read_parquet('data/raw/nger_generation_2023-24.parquet')
    LIMIT 20
""").show()

# con.sql("""
#     DESCRIBE SELECT * FROM read_csv('data/raw/cer_generation_2024-25.csv',
#                                     all_varchar = true)
# """).show()