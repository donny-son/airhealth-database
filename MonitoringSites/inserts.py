import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, select
from psycopg2.errors import UniqueViolation
from collections.abc import Iterable
from tqdm import tqdm

from models import SidoCode


AP = "postgresql://postgres:1234@localhost:5432/nccdb"
PARAMS = {'adm_cd': '11', 'year': 2000}
ENGINE = create_engine(AP)


def insert_AirKoreaMonitoringSites(csv_file):
    '''
    Params:
        csv_file: *.csv
    '''
    TBL_NAME = 'AIR_KOREA_MONITORING_SITES'
    sido_code_df = requester.get_sido_adm_cd(to_tabular=True)
    try:
        sido_code_df.to_sql(TBL_NAME, engine, index_label='id', if_exists='append')
    except Exception as e:
        if e.orig.pgcode == '23505':
            print(f"{TBL_NAME} table already inserted")
        else:
            print(f"Error while inserting {TBL_NAME}:", e)
        return -1


if __name__=="__main__":
    insert_SidoCode(REQ, ENGINE)
    insert_SidoBorder(REQ, ENGINE, year = range(2000, 2021)) # TODO:: response text error on year 2005
    # insert_SidoBorder(REQ, ENGINE, year = 2000)