from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import geopandas as gpd

from SGIS.models import SidoBorder, EmdBorder, SggBorder
from credentials.database import AP

db_connection_url = AP
engine = create_engine(db_connection_url)
Session = sessionmaker(bind=engine)

s = Session()

a = s.query(SidoBorder).first()
print(a)