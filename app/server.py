from database import Car, session
from sqlalchemy import or_
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("car")

@mcp.tool()
async def fetch_data(filters: dict):

    # Começamos com a consulta base
    query = session.query(Car)

    # Criar uma lista de filtros dinâmicos
    filter_conditions = []

    for key, value in filters.items():
        # Verifica se o filtro existe na classe Car e se o valor não é None ou vazio
        if hasattr(Car, key) and value:
            filter_conditions.append(getattr(Car, key).ilike(value))  # Usando ilike para insensibilidade a maiúsculas/minúsculas

    # Usando or_ para combinar os filtros com "OU"
    if filter_conditions:
        query = query.filter(or_(*filter_conditions))  # Passa todos os filtros com OR

    # Imprime a consulta gerada (para debugging)
    print("Consulta gerada:", str(query))

    # Executamos a consulta
    cars = query.all()

    # Verificando se encontramos resultados
    if cars:
        print("Carros encontrados:")
        results = []
        for car in cars:
            results.append(f"{car.model} - {car.year} - {car.color} - {car.fuel} - {car.brand} - {car.mileage} - {car.doors} - {car.transmission} - {car.price} - {car.status}")
        # print(results)
        return "\n".join(results)
    else:
        print("Nenhum carro encontrado para os critérios informados.")
        return "Nenhum carro encontrado."

if __name__ == "__main__":
    print('Rodando server...')
    # Initialize and run the server
    mcp.run(transport='stdio')