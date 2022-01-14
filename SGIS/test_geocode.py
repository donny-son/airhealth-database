from tkinter.messagebox import QUESTION
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

from api import SGISRequest

DO_REQUEST = True
AP = "postgresql://postgres:1234@localhost:5432/nccdb"
CSV = '/Users/dongookson/Code/data-project/SGIS/key_locations/ad8.csv'
QUERY = 'select * from key_locations'

engine = create_engine(AP)
df = pd.read_csv(CSV)

if DO_REQUEST:
    requester = SGISRequest()

    patient_locs = [requester.geocode_addr(patient) for patient in df['Address']]

    df['x'] = [p.get('x') for p in patient_locs]
    df['y'] = [p.get('y') for p in patient_locs]

    gdf = gpd.GeoDataFrame(
            df,
            crs={'init':'epsg:5179'}, 
            geometry=gpd.points_from_xy(x=df.x, y=df.y)
        )

    print(f'{gdf=}')

    gdf.to_postgis(
        'key_locations',
        engine
    )

gdf = gpd.read_postgis(QUERY, engine, geom_col='geometry')
print(gdf.head(10))
print(gdf.crs)