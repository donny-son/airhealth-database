---
title: Data Aggregation Guideline for Air Pollutant Prediction Models
author: Dongook Son, Woohyeon Lee
date: 2021-11-04
---

# Data Aggregation and Cloud Database Guideline for Air Pollutant Prediction Models

## Introduction

This article contains updates for the vastly detailed data aggregation manual originally written by Gyuheon Yang and additional concepts/features to automate the collection and migration of these data into an aggregated cloud-based database or datalake.

The cloud service provider will be AWS, as it offers affordable baremetal instances to serverless functions that can automate data cleaning process. Also, researchers can later on easily/rapidly load data from the Virtual Private Cloud(VPC) with an hosted web-based RStudio or Juptyer EC2 instance without the need for configuring their local machines. 


Geographic variables are comprised of the following data,

- Traffic
    - Road network: Distance to nearset roads, sum of road lengths
    - Vehicle registration
- Demographics(Census)
    - People
    - Households
    - Housing Buildings: # of housing buildings by type and construction year
    - Companies: # of companies & employees 
- Land Use(Land cover map)
    - proportion of residential, industrial, commercial, cultural, transportation, public facilities,agriculture,forestation,grassland, wetland, bareground, water

- Transportation Facilities
    - distances to the nearest to,
        - railroad, subway stations
        - bustop
        - airport
        - major ports
- Physical Geography
    - distances to
        - river
        - coastline
        - DMZ
- Emission
    - proportions of major pollutants(CO, NOX, SOX, TSP, PM10, VOC, NH3)
- Vegetation
    - Annual summary of NDVI
    - Median value in August for previous, current and following years
- Altitude
    - Absolute elevation
    - Proportion of concentric elevation points above or below 20/50m. 


The following table from the previous guideline[^1] illustrates the data source and format for the data above.
![[Screen Shot 2021-11-04 at 21.48.13.png]]

## Data Accumulation

### Traffic
1. Login to [KTDB](https://www.ktdb.go.kr/)
2. 정보공개 > 자료신청
	1. 교통망 GIS DB
	2. 전국
	3. Select desired year
3. 신청서 작성
	1. 신청유형 > 개인연구, 논문, 개인활용
	2. 기본정보 입력
	3. 통계자료 활동분야 > 교통량 분석, 원단위 적용, 기초현황 분석, 참고자료
	4. 통계자료 사용목적 
		1. 자료사용목적 : 미세먼지 대기오염 예측 모델 구축 연구 활용
		2. 자료제공사례 공개여부 : 공개
		3. 자료사용기간 : 신청당일로부터 약 한달 선택
4. After validation, extract `TM-KA_MR-LLV2` link data.
5. Create a file called `TM_SINGLE_POINT` and paste the following content.
	```bash
	$ touch TM_SINGLE_POINT.prj
	$ vi TM_SINLE_POINT.prj
	PROJCS["Tokyo_Transverse_Mercator",GEOGCS["GCS_Tokyo" ,DATUM["D_Tokyo",SPHEROID["Bessel_1841",6377397.155,299 .1528128]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532 925199433]],PROJECTION["Transverse_Mercator"],PARAMETE R["False_Easting",400000.0],PARAMETER["False_Northing",60 0000.0],PARAMETER["Central_Meridian",128.0000],PARAMET ER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin", 38.0],UNIT["Meter",1.0]]
	```

6. Extract MR1, MR2, Other(All roads)
	1. MR1 : highway(`101`), city highway(`102`)
	2. MR2 : $101 \cup 102 \cup LANES \ge 6$
	3. All roads : All other roads

*[UPDATE]*

If you have requested years of data in bulk and the requested data contains spatial information regarding the Metroplotian area, download scripting is required since the batch download tool does not work. 
![[Screen Shot 2021-11-06 at 5.43.32.png]]





### Vehicle Registration
1. https://stat.molit.go.kr/portal/main/portalMain.do
2. 교통/물류 > 승인통계 > 자동차등록현황보고 > 자동차등록대수_시도별 > 관련파일
http://stat.molit.go.kr/portal/cate/statFileView.do?hRsId=58&hFormId=5498&hSelectId=5498&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&month_yn=N&sFormId=5498&sStart=202109&sEnd=202109&sStyleNum=2&EXPORT=
3. Unlike the previous guideline, downloading the `canvas` is unavailable. 

### Census

### Landuse

### Railroads

### Airport, Ports

### Bus stops

### NDVI

### Emission

### Altitude




---

## Reference

[^1]: Computation of geographic variables for airpollution prediction models in South Korea, Eum, 2015
[^2]: Geodatabase: Best Practices, Flanagan M., ESRI Federal GIS conference, 2019
