from urls import URLS
from pathlib import Path

import geopandas as gpd
import requests
from yaml import safe_load
from pandas import json_normalize
from tqdm import tqdm


class SGISRequest:
    # PROD: when entry point is main.py
    # CREDENTIAL_PATH = Path(".") / "credentials" / "credentials.yml"

    # DEBUG: current file is execultable
    _SGIS = Path(__file__).parent.resolve()
    _PRJ = _SGIS.parent.resolve()
    CREDENTIAL_PATH = _PRJ / 'credentials' / 'credentials.yml'

    def __init__(self):
        self.URLS = URLS

    @property
    def token(self):
        return self.get_token(self.URLS["AUTH"])

    def get_token(self, auth_url):
        credentials = {"consumer_key": None, "consumer_secret": None}
        with open(self.CREDENTIAL_PATH) as stream:
            _credentials = safe_load(stream)
            credentials["consumer_key"] = _credentials['sgis']['consumer_key']
            credentials["consumer_secret"] = _credentials['sgis']['consumer_secret']
        response = requests.get(auth_url, params=credentials)
        token = response.json()['result']['accessToken']
        return token

    def get_gdf(self, result):
        columns = ["cd", "addr_name", "full_addr"]
        geo_columns = ["x_coor", "y_coor"]
        df = json_normalize(result)
        gdf = gpd.GeoDataFrame(df[columns], geometry=gpd.points_from_xy(df.x_coor, df.y_coor))
        gdf = gdf.set_crs("epsg:5179")  # utm-k

        return gdf

    def get_sido_adm_cd(self, to_tabular=False):
        params = {
            "accessToken": self.token,
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

    def get_adm_cd(self, cd=None, include_border=False, to_tabular=False):
        params = {
            "accessToken": self.token,
            "cd": cd,
            "pg_yn": 1 if include_border else 0
        }
        response = requests.get(self.URLS["STAGE"], params=params).json()
        if not to_tabular:
            return response
        else:
            return self.get_gdf(response["result"])

    def get_adm_border(self, year=2017, adm_cd=11, low_search=2):
        params = {
            "accessToken": self.token,
            "year": year,
            "adm_cd": adm_cd,
            "low_search": low_search
        }
        response = requests.get(self.URLS["HADMAREA"], params=params)
        return response.json()

    def get_hangjungdong_all(self, include_border=False):
        """
        :param include_border: 경계포함유무
        :return: 모든 읍면동(행정동) 리스트
        """
        token = self.token
        pg_yn = 1 if include_border else 0

        # 시도 리스트
        params = {"accessToken": token, "cd": None, "pg_yn": pg_yn}
        response = requests.get(self.URLS["STAGE"], params=params).json()
        sido_cd_list = [sido["cd"] for sido in response["result"]]
        print("시도 정보 API 호출 완료")

        # 시군구 리스트
        sigungu_cd_list = []
        for sido_cd in tqdm(sido_cd_list, desc="시군구 정보 API 호출"):
            params["cd"] = sido_cd
            response = requests.get(self.URLS["STAGE"], params=params).json()
            sigungu_cd_list += [sigungu["cd"] for sigungu in response["result"]]

        # 행정동(읍면동) 리스트
        hangjungdong_list = []
        for sigungu_cd in tqdm(sigungu_cd_list, desc="읍면동 정보 API 호출"):
            params["cd"] = sigungu_cd
            response = requests.get(self.URLS["STAGE"], params=params).json()
            hangjungdong_list += response["result"]

        return self.get_gdf(hangjungdong_list)


if __name__ == "__main__":
    sgis = SGISRequest()
    # print(f"{SGISRequest().get_sido_adm_cd(to_tabular=True)=}")
    # print(f"{SGISRequest().get_adm_cd(cd=11, include_border=1, to_tabular=True)}")
    # print(f"{SGISRequest().get_adm_border()=}")
    print(sgis.get_hangjungdong_all())
