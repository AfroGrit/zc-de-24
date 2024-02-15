#!/usr/bin/env python
# coding: utf-8

"""
This script ingests CSV data into a Postgres database. It uses command line arguments to get the necessary information such as user, password, host, port, database name, table name, and the URL of the CSV file.
"""

import os
import argparse
import sys

from time import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def main(params):
    """
    Main function that handles the data ingestion process.
    """
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Error checking for wget command
    if os.system(f"wget {url} -O {csv_name}") != 0:
        print("Error in downloading the file. Please check the URL.")
        sys.exit(1)

    try:
        engine = create_engine(
            f'postgresql://{user}:{password}@{host}:{port}/{db}')
    except SQLAlchemyError as e:
        print(f"Error in creating engine: {e}")
        sys.exit(1)

    try:
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        sys.exit(1)

    try:
        df = next(df_iter)
    except StopIteration:
        print("The file is empty.")
        sys.exit(1)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    try:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')
    except SQLAlchemyError as e:
        print(f"Error in writing to database: {e}")
        sys.exit(1)

    while True:
        try:
            t_start = time()

            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' %
                  (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
        except SQLAlchemyError as e:
            print(f"Error in writing to database: {e}")
            sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    args_list = [
        ('--user', 'user name for postgres'),
        ('--password', 'password for postgres'),
        ('--host', 'host for postgres'),
        ('--port', 'port for postgres'),
        ('--db', 'database name for postgres'),
        ('--table_name', 'name of the table where we will write the results to'),
        ('--url', 'url of the csv file')
    ]

    for arg, help_text in args_list:
        parser.add_argument(arg, required=True, help=help_text)

    args = parser.parse_args()
    main(args)