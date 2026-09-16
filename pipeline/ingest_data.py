import pandas as pd
from sqlalchemy import create_engine
import sys
from tqdm.auto import tqdm


def run():
    year = 2021
    month = 1
    pg_user = "root"
    pg_password = "root"
    pg_host = "localhost"
    pg_database = "ny_taxi"
    pg_port = 5432
    chunk_size = 100000
    target_table = "yellow_taxi_data"
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )

    first = True

    for temp_df in tqdm(df_iter):
        # calculation = ((len(temp_df) + prev_len) / len(df)) * 100
        if first:
            temp_df.head(n=0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first = False

        temp_df.to_sql(
            name=target_table, 
            con=engine, 
            if_exists='append'
        )
    print("\nProcessing complete.")

if __name__ == "__main__":
    run()