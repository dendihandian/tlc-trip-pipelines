from pandas import read_parquet
from pandas import DataFrame
from hashlib import md5

def create_df(records_dict: dict = {}):
    return DataFrame(records_dict)

def generate_md5(df: DataFrame, columns_to_hash: list = None):
    if columns_to_hash is None:
        columns_to_hash = df.columns.tolist()
    
    combined_series = df.astype(str).apply(lambda x: '|'.join(str(x)), axis=1)
    
    df['_md5'] = combined_series.apply(
        lambda x: md5(x.encode('utf-8')).hexdigest()
    )

    return df