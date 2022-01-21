import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, select
from psycopg2.errors import UniqueViolation
from collections.abc import Iterable
from tqdm import tqdm

from api import SGISRequest
from models import SidoCode


AP = "postgresql://postgres:1234@localhost:5432/nccdb"
PARAMS = {'adm_cd': '11', 'year': 2000}
ENGINE = create_engine(AP)
REQ = SGISRequest()


def insert_SidoCode(requester, engine):
    '''
    Params:
        requester: SGISRequest class
        engine: sqlalchemy.engine.base.Engine
    '''
    TBL_NAME = 'SIDO_CODE'
    try:
        sido_code_df = requester.get_sido_adm_cd(to_tabular=True)
        sido_code_df.to_sql(TBL_NAME, engine, index_label='id', if_exists='append')
    except Exception as e:
        if e.orig.pgcode == '23505':
            print(f"{TBL_NAME} table already inserted")
        else:
            print(f"Error while inserting {TBL_NAME}:", e)
        return -1


def insert_SidoBorder(requester, engine, year):
    '''
    Params:
        requester: SGISRequest class
        engine: sqlalchemy.engine.base.Engine
        year: 2000, 2001, ..., 2020, or List[int]
    '''
    TBL_NAME = f'SIDO_BORDER'
    if isinstance(year, Iterable):
        for y in year:
            print(f'Trying year => {y}')
            try:
                insert_SidoBorder(requester, engine, year=y)
            except Exception as e:
                print(f"Error while inserting {y=}:", e)
    else:
        sido_codes = engine.execute(select(SidoCode.cd, SidoCode.id)).fetchall()
        for cd, id in tqdm(sido_codes, desc='시도코드별 API 호출 & DB Insert'):
            response = requester.get_adm_border(year=year, adm_cd=cd)
            if (features := response.get('features')):
                gdf = gpd.GeoDataFrame.from_features(features, crs=5179)
                gdf['wkt_point_5179'] = gpd.points_from_xy(x=gdf.x, y=gdf.y, crs=5179)
                gdf['wkt_4326'] = gdf.to_crs(4326)['geometry']
                gdf['sido_cd_id'] = id
                gdf['year'] = year
                gdf.drop(columns=['x', 'y'], inplace=True)
                gdf.to_postgis(TBL_NAME, engine, if_exists='append', index_label='id')
                del gdf


if __name__=="__main__":
    insert_SidoCode(REQ, ENGINE)
    insert_SidoBorder(REQ, ENGINE, year = range(2000, 2021)) # TODO:: response text error on year 2005
    # insert_SidoBorder(REQ, ENGINE, year = 2000)