# PostGIS Data Modeling

## About

This documentation handles database-related modeling decisions and configuration.

## Docker

- [Official Documentation - GitHub](https://github.com/postgis/docker-postgis)
- [Official Documentation - Docker Hub](https://hub.docker.com/r/postgis/postgis)

```bash
docker run --name ncc-postgis \
  -e POSTGRES_PASSWORD="1234" \
  -e POSTGRES_DB="nccdb" \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v <localdir>:/var/lib/postgresql/data \
  -P -p 127.0.0.1:5555:5432 \
  -d postgis/postgis
```

### Testing connection

From mac terminal,

```bash

pgcli postgresql://postgres:POSTGRES_PASSWORD@localhost:5555/postgres
```

Then create spatial database with the following commands:
```sql
CREATE DATABASE mydatabase TEMPLATE template_postgis;
```

## Python <-> Docker PostGIS container

Table can be created directly from the geopandas dataframe object to the PostGIS container via sqlalchemy:

```python
import geopandas as gpd
from sqlalchemy import create_engine
import pandas as pd

d = {'col1': ['name1', 'name2'], 'wkt': ['POINT (1 2)', 'POINT (2 1)']}
df = pd.DataFrame(d)
gs = gpd.GeoSeries.from_wkt(df['wkt'])
gdf = gpd.GeoDataFrame(df['col1'], geometry=gs, crs="EPSG:4326")

engine = create_engine("postgresql://postgres:POSTGRES_PASSWORD@localhost:5432/mydatabase")  

# Create table in database	
gdf.to_postgis('test', engine)
```

Querying the table is done via the following way:

```python
read_gdf = gpd.read_postgis('select * from test', engine, geom_col='geometry')
print(read_gdf)
```