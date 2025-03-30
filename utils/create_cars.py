from faker import Faker
from faker_vehicle import VehicleProvider
from random import choice
from pathlib import Path
import sys

PROJECT_BASE_DIR = Path(__file__).parent.parent # Selecionando a raiz do projeto
sys.path.append(str(PROJECT_BASE_DIR))

# Configurando a biblioteca Faker
fake = Faker('pt_BR')
fake.add_provider(VehicleProvider)

if __name__ == '__main__':
    from app.database import Car, session

    for _ in range(100):
        mileage = choice([0, 50000, 150000, 200000])  # Quilometragem fixa
        status = "Novo" if mileage == 0 else "Usado"  # Define o status antes de criar o objeto
        car = Car(
            model = fake.vehicle_make_model(),
            year = int(fake.vehicle_year()),
            fuel = fake.random_element(elements=("Gasolina", "Álcool", "Diesel", "Elétrico")),
            brand = fake.vehicle_make(),
            color = choice(["Azul", "Vermelho", "Amarelo", "Preto", "Branco", "Prata", "Cinza", "Verde", "Laranja", "Violeta"]),
            mileage = mileage,
            doors = choice([2, 4]),
            transmission = choice(["Manual", "Automático"]),
            price = f"R$ {fake.random_int(min=5000, max=150000):,.2f}",  # Formato em reais
            status = status
        )
        session.add(car)
        session.commit()