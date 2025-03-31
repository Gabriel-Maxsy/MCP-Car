from pathlib import Path
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# Definindo a raiz do projeto:
ROOT_PATH = Path(__file__).parent.parent

# Garantindo que o diretório 'data' exista:
data_dir = ROOT_PATH / 'data'
data_dir.mkdir(parents=True, exist_ok=True)  # Cria o diretório, se não existir

# Criando a sessão para o banco de dados:
db = create_engine(f"sqlite:///{ROOT_PATH / 'data' / 'cars.db'}")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela do banco de dados:
class Car(Base):
    __tablename__ = "cars"

    id = Column("id", Integer, primary_key=True, autoincrement=True)  # ID do carro
    model = Column("model", String)  # Modelo do carro
    year = Column("year", Integer)  # Ano de fabricação
    fuel = Column("fuel", String)  # Tipo de combustível
    brand = Column("brand", String)  # Marca do carro
    color = Column("color", String)  # Cor do carro
    mileage = Column("mileage", Integer)  # Quilometragem do carro
    doors = Column("doors", Integer)  # Número de portas
    transmission = Column("transmission", String)  # Tipo de transmissão (manual, automática)
    price = Column("price", Integer)  # Preço do carro
    status = Column("status", String)  # Status do carro: novo, usado, "velho"

Base.metadata.create_all(bind=db)  # Criação do banco de dados