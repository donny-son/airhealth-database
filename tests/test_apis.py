import unittest
# RUN AS MODULE
# python3 -m tests.test_monitoring_sites

# from typing import List
# import pandas as pd
# import geopandas as gpd
# from sqlalchemy import create_engine
# from shapely.geometry.multipolygon import MultiPolygon
# from tqdm import tqdm
# from sqlalchemy.orm import sessionmaker


from SGIS.api import *
# from credentials.database import AP



class TestSGISApis(unittest.TestCase):

    r = SGISRequest()

    def test_get_token(self):
        response = self.r.get_token(self.r.URLS['AUTH'])
        self.assertIsInstance(response, str)

    def test_get_sido_adm_cd(self):
        response = self.r.get_sido_adm_cd(to_tabular=False)
        answer = 17 # 대한민국은 17개의 시도로 구분되어있음
        self.assertEqual(len(response['result']), answer)

    def test_get_adm_cd(self):
        response = self.r.get_adm_cd(cd=11230, include_border=False, to_tabular=False)
        answer = 22 # 강남구(11230)는 22개의 작은 행정동으로 이루어져있음
        self.assertEqual(len(response['result']), answer)

    def test_geocode_addr(self):
        response = self.r.geocode_addr("대전광역시 서구 청사로 189")
        answer = {'x': '989980.430867885', 'y': '1818521.44932126'}
        self.assertEqual(response, answer)

    def test_get_population(self):
        response = self.r.get_population(year=2000, gender=0, adm_cd=11, low_search=0)
        answer = [{'adm_cd': '11', 'adm_nm': '서울특별시', 'avg_age': '50.8', 'population': '9687172'}]
        self.assertEqual(response['result'], answer)

    def test_get_household(self):
        response = self.r.get_household(year=2000, adm_cd=11, low_search=0, household_type='01', ocptn_type='1')
        answer = [{'family_member_cnt': 282488, 'adm_cd': '11', 'adm_nm': '서울특별시', 'avg_family_member_cnt': '2.1', 'household_cnt': '136132'}]
        self.assertEqual(response['result'], answer)

    def test_get_house(self):
        response = self.r.get_household(year=2000, adm_cd=11230, low_search=0)
        answer = [{'family_member_cnt': 510151, 'adm_cd': '11230', 'adm_nm': '강남구', 'avg_family_member_cnt': '3', 'household_cnt': '171078'}]
        self.assertEqual(response['result'], answer)

    def test_get_company(self):
        response = self.r.get_company(year=2000, adm_cd=11230, low_search=1)
        answer = 22 # 강남구(11230)는 22개의 작은 행정동으로 이루어져있음
        self.assertEqual(len(response['result']), answer)


if __name__ == '__main__':
    unittest.main()