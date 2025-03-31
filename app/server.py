from database import Car, session
from sqlalchemy import or_
from mcp.server.fastmcp import FastMCP

# Inicialização do servidor MCP:
mcp = FastMCP("car")

# Função para consulta no banco:
@mcp.tool()
async def fetch_data(filters: dict):

    # Começamos com a consulta base:
    query = session.query(Car)

    # Criando uma lista de filtros dinâmicos:
    filter_conditions = []

    for key, value in filters.items():
        # Verifica se o filtro existe na classe Car e se o valor não é None ou vazio:
        if hasattr(Car, key) and value:
            if key == "price":
                # Verifica se o preço do carro é menor ou igual ao valor máximo informado:
                filter_conditions.append(getattr(Car, key) <= float(value))
            else:
                filter_conditions.append(getattr(Car, key).ilike(value))

    # Usando or_ para combinar os filtros com "OU":
    if filter_conditions:
        query = query.filter(or_(*filter_conditions))

    # Executando a consulta:
    cars = query.all()

    # Verificando se encontramos resultados:
    if cars:
        results = []
        # Para cada carro encontrado, formata a resposta:
        for car in cars:
            results.append(
                f"\n{'='*40}\n"
                f"ID: {car.id}\n"
                f"🚗 Modelo: {car.model}\n"
                f"📅 Ano: {car.year}\n"
                f"🎨 Cor: {car.color}\n"
                f"⛽ Combustível: {car.fuel}\n"
                f"🏭 Marca: {car.brand}\n"
                f"📏 Quilometragem: {car.mileage} km\n"
                f"🚪 Portas: {car.doors}\n"
                f"⚙️ Transmissão: {car.transmission}\n"
                f"💰 Preço: R${car.price:,.2f}\n"
                f"📌 Status: {car.status}\n"
                f"{'='*40}"
            )
        return "\n".join(results)
    else:
        return "Nenhum carro encontrado."

# Iniciando o servidor MCP:
mcp.run(transport='stdio')