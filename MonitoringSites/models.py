from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, Text, Column, ForeignKey
from geoalchemy2 import Geometry
import pandas as pd

AP = "postgresql://postgres:1234@localhost:5432/nccdb"

Base = declarative_base()
engine = create_engine(AP)

class MonitoringSite(Base):
    __tablename__ = 'MONITORING_SITES'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer)
    cd = Column(Text)
    addr_name = Column(Text)

    lower_adm_cd = relationship("SidoBorder", back_populates='higher_adm_cd')

    def __repr__(self):
        return f"Sido(id={self.id}, cd={self.cd}, addr_name={self.addr_name})"

if __name__=="__main__":
    # Create schema
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)