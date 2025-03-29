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
            results.append(
                f"\n{'='*40}\n"
                f"🚗 Modelo: {car.model}\n"
                f"📅 Ano: {car.year}\n"
                f"🎨 Cor: {car.color}\n"
                f"⛽ Combustível: {car.fuel}\n"
                f"🏭 Marca: {car.brand}\n"
                f"📏 Quilometragem: {car.mileage} km\n"
                f"🚪 Portas: {car.doors}\n"
                f"⚙️ Transmissão: {car.transmission}\n"
                f"💰 Preço: R$ {car.price}\n"
                f"📌 Status: {car.status}\n"
                f"{'='*40}"
            )
        # print("\n".join(results))
        return "\n".join(results)
    else:
        print("Nenhum carro encontrado para os critérios informados.")
        return "Nenhum carro encontrado."

if __name__ == "__main__":
    print('Rodando server...')
    # teste = {
    #     "color": "Azul",
    #     "brand": "Ford"
    # }
    # fetch_data(teste)
    # Initialize and run the server
    mcp.run(transport='stdio')