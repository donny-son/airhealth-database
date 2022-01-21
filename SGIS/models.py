from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, Text, Column, ForeignKey
from geoalchemy2 import Geometry
import pandas as pd

AP = "postgresql://postgres:1234@localhost:5432/nccdb"

Base = declarative_base()
engine = create_engine(AP)

class SidoCode(Base):
    __tablename__ = 'SIDO_CODE'

    id = Column(Integer, primary_key=True)
    cd = Column(Text)
    addr_name = Column(Text)

    lower_adm_cd = relationship("SidoBorder", back_populates='higher_adm_cd')

    def __repr__(self):
        return f"Sido(id={self.id}, cd={self.cd}, addr_name={self.addr_name})"



class SidoBorder(Base):

    __tablename__ = f'SIDO_BORDER'

    id = Column(Integer, primary_key=True)
    sido_cd_id = Column(Integer, ForeignKey('SIDO_CODE.id'))
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    geometry = Column(Geometry(srid=5179))
    wkt_point_5179 = Column(Text)
    wkt_4326 = Column(Text)
    year = Column(Integer, nullable=False)

    higher_adm_cd = relationship("SidoCode", back_populates="lower_adm_cd")

    def __repr__(self):
        return f"SidoBorder(id={self.id}, adm_cd={self.adm_cd}, adm_name={self.adm_name}, year={self.year})"


if __name__=="__main__":
    # Create schema
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)