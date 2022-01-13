from urls import URLS
from pathlib import Path

import geopandas as gpd
import requests
from yaml import safe_load
from pandas import json_normalize



class SGISRequest:

    # PROD: when entry point is main.py
    # CREDENTIAL_PATH = Path(".") / "credentials" / "credentials.yml"

    # DEBUG: current file is execultable
    _SGIS = Path(__file__).parent.resolve()
    _PRJ = _SGIS.parent.resolve()
    CREDENTIAL_PATH = _PRJ / 'credentials' / 'credentials.yml'

    def __init__(self):
        self.URLS = URLS
        self.TOKEN = self.get_token(self.URLS["AUTH"])

    def get_token(self, auth_url):
        credentials = {"consumer_key": None, "consumer_secret": None}
        with open(self.CREDENTIAL_PATH) as stream:
            _credentials = safe_load(stream)
            credentials["consumer_key"] = _credentials['sgis']['consumer_key']
            credentials["consumer_secret"] = _credentials['sgis']['consumer_secret']
        response = requests.get(auth_url, params=credentials)
        token = response.json()['result']['accessToken']
        return token

    def get_sido_adm_cd(self, to_tabular=False):
        params = {
                "accessToken": self.TOKEN,
                "cd": None,
                "pg_yn": 0
                }
        response = requests.get(self.URLS["STAGE"], params=params)
        if not to_tabular:
            return response.json()
        else:
            _response = response.json()
            _result = _response["result"]
            columns = ["cd", "addr_name"]
            df = json_normalize(_result)
            return df[columns]

    def get_adm_cd(self, cd=None, include_border=0, to_tabular=False):
        params = {
                "accessToken": self.TOKEN,
                "cd": cd,
                "pg_yn": include_border
                }
        response = requests.get(self.URLS["STAGE"], params=params)
        if not to_tabular:
            return response.json()
        else:
            _response = response.json()
            _result = _response["result"]
            columns = ["cd", "addr_name", "full_addr"]
            geo_columns = ["x_coor", "y_coor"]
            df = json_normalize(_result)
            gdf = gpd.GeoDataFrame(df[columns], geometry=gpd.points_from_xy(df.x_coor, df.y_coor))
            gdf = gdf.set_crs("epsg:5179") #utm-k
            return gdf

    def get_adm_border(self, year=2017, adm_cd=11, low_search=2):
        params = {
                "accessToken": self.TOKEN,
                "year": year,
                "adm_cd": adm_cd,
                "low_search": low_search
                }
        response = requests.get(self.URLS["HADMAREA"], params=params)
        return response.json()

    def geocode_addr(self, address: str, xy_only: bool) -> dict:
        """geocode string address to utmk coord

        Args:
            address (str): "대전광역시 서구 청사로 189"
        """
        params = {
                "accessToken": self.TOKEN,
                "address": address,
                }
        response = requests.get(self.URLS["GEOCODING"], params=params)
        if xy_only:
            _result = response.json().get('result')
            if int(_result.get("totalcount")) > 1:
                raise Warning("Multiple (x,y) returned. Check which (x,y) is correct. Defaults to using the first pair.")
            _first = _result.get("resultdata")[0]
            return {'x':_first.get('x'), 'y':_first.get('y')}
        return response.json()


if __name__ == "__main__":
    # print(f"{SGISRequest().get_sido_adm_cd(to_tabular=True)=}")
    # print(f"{SGISRequest().get_adm_cd(cd=11, include_border=1, to_tabular=True)}")
    # print(f"{SGISRequest().get_adm_border()=}")
    res = SGISRequest().geocode_addr('서울특별시 강남구 역삼로 92길 12', xy_only=True)
    print(f"{type(res)=}")
    print(f"{res=}")
