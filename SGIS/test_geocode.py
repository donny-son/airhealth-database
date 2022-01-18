import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import box

from api import SGISRequest

AP = "postgresql://postgres:1234@localhost:5432/nccdb"
CSV = '/Users/dongookson/Code/data-project/SGIS/key_locations/ad8.csv'
QUERY = 'select * from key_locations'
GET = False

# connect to database AP
engine = create_engine(AP)

if GET:
    # read dummy data
    df = pd.read_csv(CSV)[0:10]

    # Make API GET request 
    patient_locs = [SGISRequest().geocode_addr(patient) for patient in df['Address']]
    df['x_5179'] = [p.get('x') for p in patient_locs]
    df['y_5179'] = [p.get('y') for p in patient_locs]

    # create geodataframe
    gdf = gpd.GeoDataFrame(
            df,
            crs='epsg:5179', 
            geometry=gpd.points_from_xy(x=df.x_5179, y=df.y_5179)
        )

    # create well-known-text(wkt) column for WGS84
    gdf['wkt_4326'] = gdf.to_crs(4326)['geometry']

    # write as table
    gdf.to_postgis(
        'key_locations',
        engine
    )
else:
    gdf = gpd.read_postgis(QUERY, engine, geom_col='geometry')
    print(gdf.head(10))
    # print(gdf.crs)
    # print(gdf['geometry'].sindex.query(box(988969.330849867, 988969.33084999, 1818020.086700, 1818020.0860560)))
    # print(type(gdf['geometry']))