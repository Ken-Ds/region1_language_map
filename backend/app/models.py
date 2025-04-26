# app/models.py

from pydantic import BaseModel

class Language(BaseModel):
    LANGUAGE_ID: str
    NAME: str

class Dialect(BaseModel):
    DIALECT_ID: str
    DIALECT_NAME: str
    LANGUAGE_ID: str

class Municipality(BaseModel):
    MUNICIPALITY_ID: str
    NAME: str
    INFORMATION: str
    PROVINCE_ID: str

class MunicipalityLanguage(BaseModel):
    MUNICIPALITY_ID: str
    LANGUAGE_ID: str
    DIALECT_ID: str

class Phrase(BaseModel):
    PHRASE_ID: str
    CONTENT: str
    LANGUAGE_ID: str

class ProvinceLanguage(BaseModel):
    PROVINCE_ID: str
    DIALECT_ID: str
    PERCENTAGE: float

class Province(BaseModel):
    PROVINCE_ID: str
    NAME: str
    INFORMATION: str

class Popular(BaseModel):
    POPULAR_ID: str
    NAME: str
    TYPE: str
    LOCATION: str
    PROVINCE_ID: str