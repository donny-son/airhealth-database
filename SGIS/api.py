from pathlib import Path

import geopandas as gpd
import requests
from yaml import safe_load
from pandas import json_normalize
from tqdm import tqdm

# RUN AS MODULE
from SGIS.endpoints import URLS


class SGISRequest:

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

    def get_sido_adm_cd(self, cd=None, to_tabular=False):
        params = {
            "accessToken": self.token,
            "cd": cd,
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
            return get_gdf(response["result"])

    def get_adm_border(self, year=2017, adm_cd=11, low_search=2):
        params = {
            "accessToken": self.token,
            "year": year,
            "adm_cd": adm_cd,
            "low_search": low_search
        }
        response = requests.get(self.URLS["HADMAREA"], params=params)
        return response.json()

    def geocode_addr(self, address: str, xy_only=True) -> dict:
        """geocode string address to utmk coord

        Args:
            address (str): "대전광역시 서구 청사로 189"
        """
        params = {
                "accessToken": self.token,
                "address": address,
                }
        response = requests.get(self.URLS["GEOCODING"], params=params)
        if xy_only:
            _result = response.json().get('result')
            if _result is not None:
                if int(_result.get("totalcount")) > 1:
                    raise Warning("Multiple (x,y) returned. Check which (x,y) is correct. Defaults to using the first pair.")
                _first = _result.get("resultdata")[0]
                return {'x':_first.get('x'), 'y':_first.get('y')}
            else:
                return {'x':None, 'y':None}
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

        return get_gdf(hangjungdong_list)

    def get_population(self, year=2000, gender=None, adm_cd=None, low_search=1):
        """인구주택총조사 인구 통계 API.

        Args:
            year (int, required): List of values are 2000, 2005, 2010, 2015 ~ 2020.
            gender (int, optional): Defaults to None. 0(All), 1(Men), 2(Women)
            adm_cd (int, optional): Defaults to None. If None returns all sido information(2 digit code.). Supports 5digit SGG Code and 7digit EMD Code.
            low_search (int, optional): Defaults to 1. Returns information for 1 level lower adm_cd. If 0, returns information for the requested adm_cd. If 2, returns information for 2 level lower adm_cd, for example, if adm_cd=11 the response will get all information for the 7digit adm_cd starting with 11.
        """
        params = {
            "accessToken": self.token,
            "year": year,
            "gender": gender,
            "adm_cd": adm_cd,
            "low_search": low_search,
        }
        response = requests.get(self.URLS["POPULATION"], params=params)
        return response.json()

    def get_household(self, year=2000, adm_cd=None, low_search=1, household_type=None, ocptn_type=None):
        """인구주택총조사 가구 통계 API.

        Args:
            year (int, required): List of values are 2000, 2005, 2010, 2015 ~ 2020.

            adm_cd (int, optional): Defaults to None. If None returns all sido information(2 digit code.). Supports 5digit SGG Code and 7digit EMD Code.

            low_search (int, optional): Defaults to 1. Returns information for 1 level lower adm_cd. If 0, returns information for the requested adm_cd. If 2, returns information for 2 level lower adm_cd, for example, if adm_cd=11 the response will get all information for the 7digit adm_cd starting with 11.

            household_type: Defaults to None. The following is the table of types and codes.
                종류	      코드
                1세대가구	     01
                2세대가구	     02
                3세대가구	     03
                4세대가구        04
                5세대이상가구     05
                1인가구	        A0
                비혈연가구       B0

            ocptn_type: Defaults to None. The following is the table of types and codes.
                종류        	      코드
                자기집	                1
                전세(월세없음)	          2
                보증금 있는 월세	      3
                보증금 없는 월세	      4
                사글세	                5
                무상(관사,사택,친척집 등)	6

        """
        params = {
            "accessToken": self.token,
            "year": year,
            "adm_cd": adm_cd,
            "low_search": low_search,
            "household_type": household_type,
            "ocptn_type": ocptn_type,
        }
        response = requests.get(self.URLS["HOUSEHOLD"], params=params)
        return response.json()

    def get_house(self, year=2000, adm_cd=None, low_search=1, house_type=None, const_year=None, house_area_cd=None, house_use_prid_cd=None):
        """인구주택총조사 주택 통계 API.

        Args:
            year (int, required): List of values are 2000, 2005, 2010, 2015 ~ 2020.

            adm_cd (int, optional): Defaults to None. If None returns all sido information(2 digit code.). Supports 5digit SGG Code and 7digit EMD Code.

            low_search (int, optional): Defaults to 1. Returns information for 1 level lower adm_cd. If 0, returns information for the requested adm_cd. If 2, returns information for 2 level lower adm_cd, for example, if adm_cd=11 the response will get all information for the 7digit adm_cd starting with 11.

            house_type: Defaults to None. The following is the table of types and codes.
                종류	코드
                단독주택	01
                아파트	02
                연립주택	03
                다세대주택	04
                비거주용 건물(상가,공장,여관 등)내 주택	05
                주택이외의 거처	06

            const_year: Defaults to None. The following is the table of types and codes.
                https://sgis.kostat.go.kr/developer/html/openApi/api/dataCode/ConstYearCode.html

            house_area_cd: Defaults to None. The following is the table of types and codes.
                https://sgis.kostat.go.kr/developer/html/openApi/api/dataCode/HouseAreaCode.html

            house_use_prid_cd: Defaults to None. The following is the table of types and codes.
                https://sgis.kostat.go.kr/developer/html/openApi/api/dataCode/HouseUsePridCode.html
        """
        params = {
            "accessToken": self.token,
            "year": year,
            "adm_cd": adm_cd,
            "low_search": low_search,
            "house_type": house_type,
            "const_year": const_year,
            "house_area_cd": house_area_cd,
            "house_use_prid_cd": house_use_prid_cd,
        }
        response = requests.get(self.URLS["HOUSE"], params=params)
        return response.json()

    def get_company(self, year=2000, adm_cd=None, low_search=1, class_code=None, theme_cd=None):
        """인구주택총조사 주택 통계 API.

        Args:
            year (int, required): List of values are 2000, 2005, 2010, 2015 ~ 2020.

            adm_cd (int, optional): Defaults to None. If None returns all sido information(2 digit code.). Supports 5digit SGG Code and 7digit EMD Code.

            low_search (int, optional): Defaults to 1. Returns information for 1 level lower adm_cd. If 0, returns information for the requested adm_cd. If 2, returns information for 2 level lower adm_cd, for example, if adm_cd=11 the response will get all information for the 7digit adm_cd starting with 11.

            class_code: Defaults to None. Cannot be used with 'theme_cd' parameter. To use this API, users must run 산업분류 API to check the codes of interest.

            theme_cd: Defaults to None. The following is the table of types and codes.
                https://sgis.kostat.go.kr/developer/html/openApi/api/dataCode/ThemeCode.html
        """
        if class_code and theme_cd:
            raise ValueError('class_code and theme_cd are exclusive! choose only one!')
        params = {
            "accessToken": self.token,
            "year": year,
            "adm_cd": adm_cd,
            "low_search": low_search,
            "class_code": class_code,
            "theme_cd": theme_cd,
        }
        response = requests.get(self.URLS["COMPANY"], params=params)
        return response.json()

    
def get_gdf(result):
    columns = ["cd", "addr_name", "full_addr"]
    geo_columns = ["x_coor", "y_coor"]
    df = json_normalize(result)
    gdf = gpd.GeoDataFrame(df[columns], geometry=gpd.points_from_xy(df.x_coor, df.y_coor))
    gdf = gdf.set_crs("epsg:5179")  # utm-k

    return gdf


if __name__ == "__main__":
    sgis = SGISRequest()
    # print(f"{SGISRequest().get_sido_adm_cd(to_tabular=True)=}")
    # print(f"{SGISRequest().get_sido_adm_cd(to_tabular=True)=}")
    # print(f"{SGISRequest().get_adm_cd(cd=11, include_border=1, to_tabular=True)}")
    print(sgis.get_hangjungdong_all())

