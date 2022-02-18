import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from psycopg2.errors import UniqueViolation
from collections.abc import Iterable
from tqdm import tqdm

from api import SGISRequest
from models import SidoCode, SidoBorder


AP = "postgresql://postgres:1234@localhost:5432/nccdb"
PARAMS = {'adm_cd': '11', 'year': 2000}
ENGINE = create_engine(AP)
SESSION = sessionmaker(bind=ENGINE)
REQ = SGISRequest()


def insert_SidoCode(requester, engine):
    '''
    Params:
        requester: SGISRequest class
        engine: sqlalchemy.engine.base.Engine
    '''
    TBL_NAME = 'SIDO_CODES'
    sido_code_df = requester.get_sido_adm_cd(to_tabular=True)
    try:
        sido_code_df.to_sql(TBL_NAME, engine, index_label='id', if_exists='append')
    except Exception as e:
        if e.orig.pgcode == '23505':
            print(f"{TBL_NAME} table already inserted")
        else:
            print(f"Error while inserting {TBL_NAME}:", e)


def insert_SidoBorder(requester, engine, year, override: bool):
    '''
    Params:
        requester: SGISRequest class
        engine: sqlalchemy.engine.base.Engine
        year: 2000, 2001, ..., 2020, or List[int]
        override: if true deletes all rows for the table
    '''
    TBL_NAME = f'SIDO_BORDERS'
    if override:
        with SESSION() as s:
            s.query(SidoBorder).delete()
            s.commit()

    if isinstance(year, Iterable):
        for y in year:
            print(f'Trying year => {y}')
            try:
                insert_SidoBorder(requester, engine, year=y, override=override)
            except Exception as e:
                print(f"Error while processing year:{y}", e)
    else:
        sido_codes = engine.execute(select(SidoCode.cd, SidoCode.id)).fetchall()
        for (existing_year,) in SESSION().query(SidoBorder.year).distinct():
            if year == existing_year:
                print(f"{year} already inserted in table")
                return
        for cd, id in tqdm(sido_codes, desc='시도코드별 API 호출 & DB Insert'):
            response = requester.get_adm_border(year=year, adm_cd=cd)
            if (features := response.get('features')):
                gdf = gpd.GeoDataFrame.from_features(features, crs=5179)
                gdf['wkt_point_5179'] = gpd.points_from_xy(x=gdf.x, y=gdf.y, crs=5179)
                gdf['wkt_4326'] = gdf.to_crs(4326)['geometry']
                gdf['sido_cd_id'] = id
                gdf['year'] = year
                gdf.drop(columns=['x', 'y'], inplace=True)
                try:
                    gdf.to_postgis(TBL_NAME, engine, if_exists='append', index_label='id')
                except Exception as e:
                    print("Error on to_postgis", e)
                del gdf


if __name__=="__main__":
    # insert_SidoCode(REQ, ENGINE)
    # insert_SidoBorder(REQ, ENGINE, year = range(2000, 2021), override=True) # TODO:: response text error on year 2005
    insert_SidoBorder(REQ, ENGINE, year = 2005, override=False)
    # insert_SidoBorder(REQ, ENGINE, year = 2021, override=False)