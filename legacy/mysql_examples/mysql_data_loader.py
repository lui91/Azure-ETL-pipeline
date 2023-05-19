import pandas as pd

class DataLoader:
    def __init__(self) -> None:
        pass

    def read_parquet_file(self, path: str):
        df = pd.read_parquet(path)
        return df

    def load_to_sql(self, df : pd.DataFrame, con, table_name="flights_Fact" ,how="append"):
        df.to_sql(table_name, con=con, if_exists=how)
        print("Data successfully added")