from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, Text, Column, ForeignKey
from geoalchemy2 import Geometry
import pandas as pd

# RUN AS MODULE
from credentials.database import AP

Base = declarative_base()
engine = create_engine(AP)

class AirKoreaMonitoringSites(Base):

    __tablename__ = f'AIR_KOREA_MONITORING_SITES'

    id = Column(Integer, primary_key=True)
    site_id_no = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    station_cd = Column(Text)
    address = Column(Text)
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    hadm_cd = Column(Text)
    hadm_nm = Column(Text)
    badm_cd = Column(Text)
    badm_nm = Column(Text)
    year = Column(Integer)
    geometry = Column(Geometry(srid=5179))
    wkt_4326 = Column(Text)

    def __repr__(self):
        return f"AirKoreaMonitoringSites(site_id_no={self.site_id_no}, address={self.address}, year={self.year})"


if __name__=="__main__":
    # Create schema
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)