# %% [markdown]
# ## Exploratory Analysis

# %% [markdown]
# Import modules
# %%
import duckdb
from pathlib import Path
import pandas as pd

# %%
pd.set_option('display.max_rows', 1000)      
pd.set_option('display.max_columns', None)   
pd.set_option('display.width', 10000)        

# %%
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = f'{PROJECT_ROOT}/data/raw'

# %%
con = duckdb.connect("nem.duckdb")

# %%
df = con.sql(f"DESCRIBE SELECT * FROM '{RAW_DATA_DIR}/nger_generation_2021-22.parquet'").df()
print(df)
# %%
df = con.sql(f"""
    SELECT filename, COUNT(*) AS row_count
    FROM read_parquet('{RAW_DATA_DIR}/*.parquet', union_by_name = true, filename = true)
    GROUP BY filename
    ORDER BY filename
""").df()

print(df)


# %%
con.sql(f"""
    DESCRIBE SELECT * FROM read_parquet('{RAW_DATA_DIR}/*.parquet', union_by_name = true)
""").show()
# %% [markdown] 

