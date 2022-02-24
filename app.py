from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import geopandas as gpd
from greppo import app

import sys
sys.path.append('/Users/dongookson/Code/airhealth-database')
from credentials.database import AP
from SGIS.models import SggBorder, SidoBorder
from MonitoringSites.models import AirKoreaMonitoringSites

engine = create_engine(AP)
Session = sessionmaker(bind=engine)
s = Session()

years = list(range(2001,2021))
select_year = app.select(name="Year", options=years, default=2001)

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

q = s.query(SidoBorder).filter(SidoBorder.year==select_year)
border = gpd.GeoDataFrame.from_postgis(q.statement, q.session.bind, geom_col='geometry')
border = border.to_crs(4326)

app.overlay_layer(
    border,
    name='KOR SIDO Border',
    description="Kor SIDO border",
    style={"fillColor": "#F87979"},
    visible=False,
)

q = s.query(SggBorder).filter(SggBorder.year==select_year)
border = gpd.GeoDataFrame.from_postgis(q.statement, q.session.bind, geom_col='geometry')
border = border.to_crs(4326)

app.overlay_layer(
    border,
    name='KOR SGG Border',
    description="Kor SGG border",
    style={"fillColor": "#88c7dc"},
    visible=True,
)

q = s.query(AirKoreaMonitoringSites).filter(AirKoreaMonitoringSites.year == select_year)
sites = gpd.GeoDataFrame.from_postgis(q.statement, q.session.bind, geom_col='geometry')
sites = sites.to_crs(4326)

app.overlay_layer(
    sites,
    name='Airkorea Monitoring Sites',
    description='Airkorea Monitoring Sites',
    style={"fillColor": "#FFDA44"},
    visible=True,
)

