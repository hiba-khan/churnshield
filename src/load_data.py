import pandas as pd 
from sqlalchemy import create_engine


#connection string to your local postgres

engine  = create_engine("postgresql://postgres:123456@localhost:5432/churn_db")

#load the csv
df=pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn (3).csv")

#clean column names  - lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(" ","_")

#pusj to postgres

df.to_sql("customers", engine , if_exists= "replace",index=False)

print(f"Done! {len(df)} rows loaded into churn_db.customers")