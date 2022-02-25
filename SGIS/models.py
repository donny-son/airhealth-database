from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Integer, Text, Column, ForeignKey
from geoalchemy2 import Geometry
import pandas as pd


# RUN AS MODULE
from credentials.database import AP

Base = declarative_base()
engine = create_engine(AP)
Session = sessionmaker(bind=engine)


class SidoCode(Base):
    __tablename__ = 'SIDO_CODES'

    id = Column(Integer, primary_key=True)
    cd = Column(Text)
    addr_name = Column(Text)

    lower_adm_cd = relationship("SidoBorder", back_populates='higher_adm_cd')
    lower_adm_cd_emd = relationship("EmdBorder", back_populates='higher_adm_cd_emd')
    lower_adm_cd_sgg = relationship("SggBorder", back_populates='higher_adm_cd_sgg')

    def __repr__(self):
        return f"Sido(id={self.id}, cd={self.cd}, addr_name={self.addr_name})"


class SidoBorder(Base):

    __tablename__ = f'SIDO_BORDERS'

    id = Column(Integer, primary_key=True)
    sido_cd_id = Column(Integer, ForeignKey('SIDO_CODES.id'))
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    geometry = Column(Geometry(srid=5179))
    wkt_point_5179 = Column(Text)
    wkt_4326 = Column(Text)
    year = Column(Integer, nullable=False)

    higher_adm_cd = relationship("SidoCode", back_populates="lower_adm_cd")

    def __repr__(self):
        return f"SidoBorder(id={self.id}, adm_cd={self.adm_cd}, adm_nm={self.adm_nm}, year={self.year})"


class EmdBorder(Base):

    __tablename__ = f'EMD_BORDERS'

    id = Column(Integer, primary_key=True)
    sido_cd_id = Column(Integer, ForeignKey('SIDO_CODES.id'))
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    geometry = Column(Geometry(srid=5179))
    wkt_point_5179 = Column(Text)
    wkt_4326 = Column(Text)
    year = Column(Integer, nullable=False)

    higher_adm_cd_emd = relationship("SidoCode", back_populates="lower_adm_cd_emd")

    def __repr__(self):
        return f"EmdBorder(id={self.id}, adm_cd={self.adm_cd}, adm_nm={self.adm_nm}, year={self.year})"


class SggBorder(Base):

    __tablename__ = f'SGG_BORDERS'

    id = Column(Integer, primary_key=True)
    sido_cd_id = Column(Integer, ForeignKey('SIDO_CODES.id'))
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    geometry = Column(Geometry(srid=5179))
    wkt_point_5179 = Column(Text)
    wkt_4326 = Column(Text)
    year = Column(Integer, nullable=False)

    higher_adm_cd_sgg = relationship("SidoCode", back_populates="lower_adm_cd_sgg")

    def __repr__(self):
        return f"SggBorder(id={self.id}, adm_cd={self.adm_cd}, adm_nm={self.adm_nm}, year={self.year})"

class AdmCode(Base):

    __tablename__ = f'ADM_CODES'

    id = Column(Integer, primary_key=True)
    adm_cd = Column(Text)
    adm_nm = Column(Text)
    year = Column(Integer, nullable=False)

    def __repr__(self):
        return f"AdmCode(id={self.id}, adm_cd={self.adm_cd}, adm_nm={self.adm_nm}, year={self.year})"



if __name__=="__main__":
    # Create schema
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)