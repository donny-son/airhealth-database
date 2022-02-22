import pandas as pd
import os.path
import geopandas as gpd
from sqlalchemy import create_engine, select
from psycopg2.errors import UniqueViolation
from collections.abc import Iterable
from tqdm import tqdm


AP = "postgresql://postgres:1234@localhost:5555/nccdb"
ENGINE = create_engine(AP)

def create_long_csv(xlsx_file='MonitoringSites/assets/new_MS_2001-2019.xlsx', outfile='MonitoringSites/assets/long.csv'):
    df = pd.read_excel(xlsx_file)
    listOfDict = df.to_dict('records')

    year_columns = ['yr_2001', 'yr_2002', 'yr_2003', 'yr_2004', 'yr_2005',
        'yr_2006', 'yr_2007', 'yr_2008', 'yr_2009', 'yr_2010', 'yr_2011',
        'yr_2012', 'yr_2013', 'yr_2014', 'yr_2015', 'yr_2016', 'yr_2017',
        'yr_2018', 'yr_2019', 'yr_2020']

    result = []
    id = 1
    for d in listOfDict:
        for y in year_columns:
            if d.get(y):
                record = {}
                record['id'] = id
                record['site_id_no'] = d.get('ID')
                record['station_cd']= d.get('CODE')
                record['address']= d.get('ADD')
                record['adm_cd']= d.get('SGG_cd_rev')
                record['adm_nm']= d.get('SGG_nm_rev')
                record['hadm_cd']= d.get('HEMD_cd')
                record['hadm_nm']= d.get('HEMD_nm')
                record['badm_cd']= d.get('BEMD_cd')
                record['badm_nm']= d.get('BEMD_nm')
                record['wgs_x']= d.get('WGS_X_rev')
                record['wgs_y']= d.get('WGS_Y_rev')
                record['year']= y.split("_")[1]
                result.append(record)
                id += 1

    pd.DataFrame(result).to_csv(outfile, index=False)


def insert_AirKoreaMonitoringSites(csv_file='MonitoringSites/assets/long.csv'):
    '''
    Params:
        csv_file: *.csv
    '''
    TBL_NAME = 'AIR_KOREA_MONITORING_SITES'
    df = pd.read_csv(
        csv_file
    )
    gdf = gpd.GeoDataFrame(
        df.drop(columns=['wgs_x', 'wgs_y']), 
        geometry=gpd.points_from_xy(df.wgs_x, df.wgs_y),
        crs=5179
    )
    gdf['wkt_4326'] = gpd.points_from_xy(df.wgs_x, df.wgs_y,crs=4326)
    try:
        gdf.to_postgis(TBL_NAME, ENGINE, if_exists='append',index_label='id')
    except Exception as e:
        print(f"Error while inserting {TBL_NAME}:", e)


if __name__=="__main__":
    create_long_csv()
    insert_AirKoreaMonitoringSites()