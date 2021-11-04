---
title: Data Aggregation Guideline for Air Pollutant Prediction Models
author: Dongook Son, Woohyeon Lee
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


The following table illustrate the data source and format for the data above.


---

## Reference

 [^1] : Computation of geographic variables for airpollution prediction models in South Korea, Eum, 2015
 [^2] : Geodatabase: Best Practices, Flanagan M., ESRI Federal GIS conference, 2019
