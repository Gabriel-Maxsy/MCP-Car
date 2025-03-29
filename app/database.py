from pathlib import Path
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# Definindo a raiz do projeto
ROOT_PATH =  Path(__file__).parent.parent

db = create_engine(f"sqlite:///{ROOT_PATH / 'data' / 'cars.db'}")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela
class Car(Base):
    __tablename__ = "cars"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    model = Column("model", String) # Modelo
    year = Column("year", Integer)  # Ano
    fuel = Column("fuel", String)   # Combustível
    brand = Column("brand", String)  # Marca do carro
    color = Column("color", String)  # Cor do carro
    mileage = Column("mileage", Integer)  # Quilometragem
    doors = Column("doors", Integer)  # Número de portas
    transmission = Column("transmission", String)  # Tipo de transmissão (manual, automática)
    price = Column("price", Integer)  # Preço do carro
    status = Column("status", String) # Status do carro: novo, usado, "velho"

Base.metadata.create_all(bind=db) # Criação do banco

def get_session():
    return session