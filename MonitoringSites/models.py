from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, Text, Column, ForeignKey
from geoalchemy2 import Geometry
import pandas as pd

AP = "postgresql://postgres:1234@localhost:5432/nccdb"

Base = declarative_base()
engine = create_engine(AP)

class AirKoreaMonitoringSites(Base):

    __tablename__ = f'AIR_KOREA_MONITORING_SITES'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    geometry = Column(Geometry(srid=5179))
    wkt_point_5179 = Column(Text)
    wkt_4326 = Column(Text)
    addr_name = Column(Text)

    def __repr__(self):
        return f"AirKoreaMonitoringSites(site_id={self.site_id}, addr_name={self.addr_name}, year={self.year})"


if __name__=="__main__":
    # Create schema
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)