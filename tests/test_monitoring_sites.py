# RUN AS MODULE
# python3 -m tests.test_monitoring_sites

from typing import List
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry.multipolygon import MultiPolygon
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker


from MonitoringSites.models import AirKoreaMonitoringSites as AKMsite
from SGIS.models import SggBorder

AP = "postgresql://postgres:1234@localhost:5555/nccdb"
ENGINE = create_engine(AP)
Session = sessionmaker(ENGINE)

def get_sites(year=2001) -> gpd.GeoDataFrame:
    """returns GeoDataFrame of AirKorea Monitoring Sites of a specified year

    Args:
        year (int, optional): _description_. Defaults to 2001.

    Returns:
        gpd.GeoDataFrame: _description_
    """
    sites = []
    sites_query = Session().query(
        AKMsite.id,
        AKMsite.address, 
        AKMsite.geometry
        ).filter(AKMsite.year == year)

    for site in sites_query:
        _site = {}
        _site['id'] = site.id
        _site['address'] = site.address
        _site['geometry'] = site.geometry.desc
        sites.append(_site)

    df = pd.DataFrame(sites, columns=['id', 'address', 'geometry'])
    geom = gpd.GeoSeries.from_wkb(df['geometry'], crs=5179)
    sites = gpd.GeoDataFrame(df, geometry=geom, crs=5179)
    return sites

def get_korea(year=2001) -> MultiPolygon:
    """get korea SggBorder into a single MultiPolygon

    Args:
        year (int): 2001 ~ 2020

    Returns:
        shapely.geometry.multipolygon.MultiPolygon
    """
    sggborder_query = Session().query(SggBorder.geometry).filter(SggBorder.year == year)
    border = []
    for sggborder in sggborder_query:
        border.append(sggborder.geometry.desc)
    
    korea = gpd.GeoSeries.from_wkb(border, crs=5179)
    return korea.unary_union


def get_outliers(year=2001) -> List[dict]:
    outliers = []
    sites = get_sites(year)
    korea = get_korea(year)

    for i, site in sites.iterrows():
        d = {}
        point = site['geometry']
        if not point.within(korea):
            d['id'] = site.id
            d['year'] = year
            d['address'] = site.address
            d['geometry'] = site.geometry
            outliers.append(d)

    return outliers


if __name__=="__main__":

    result = []

    years = range(2001, 2021)
    for year in tqdm(years):
        outliers = get_outliers(year)
        if outliers:
            result.extend(outliers)

    pd.DataFrame(result).to_csv('tests/results/monitoring_sites_outliers.csv', index=False)