import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

# Definindo caminho para a conexão com o servidor:
ROOT_PATH = Path(__file__).parent.parent
SERVER_PATH = str(ROOT_PATH / 'app/server.py')

# Definindo a classe do lado do cliente:
class MCPClient:
    def __init__(self):
        # Inicializando a sessão e objetos do cliente:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    # Função para conexão com o servidor MCP:
    async def connect_to_server(self, server_teste: str):
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_teste],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

    # Processamento das respostas do usuário:
    async def process_query(self, query):
        if not self.session:
            return "Erro: Cliente não conectado ao servidor."

        # Chamando a função de consulta no banco de dados do servidor:
        result = await self.session.call_tool("fetch_data", {"filters": query})
        return result.content[0].text
        
    # Chat iterativo com o usuário:
    async def chat_loop(self):
        while True:
            try:
                fields = ["preço máximo (sem centavos para melhor busca)", "Modelo", "Ano", "Marca", "Cor"]
                query = {
                    "price": "",
                    "model": "",
                    "year": "",
                    "brand": "",
                    "color": ""
                }

                for field, key in zip(fields, query.keys()):
                    user_input = input(f"\nQual {field} você procura: ").strip()  # Solicita a entrada do usuário

                    # Verifica se o usuário quer sair:
                    if user_input.lower() == "sair":
                        print("Saindo do chat...")
                        return

                    if key == "price":
                        user_input = user_input.replace(".", "").replace(",", "")  # Limpa o valor do preço

                    # Preenche o dicionário com o valor correspondente:
                    query[key] = user_input

                response = await self.process_query(query)

                print(response)
                print("\nSe quiser procurar outra opção, sinta-se à vontade:")
            # Tratamento de erros e interrupção do chat:
            except asyncio.CancelledError:
                print("A tarefa foi cancelada.")
            except Exception as e:
                print(f"\nErro: {str(e)}")
        
# Função principal, onde conectamos com o servidor e iniciamos o chat:
async def main():
    client = MCPClient()
    try:
        await client.connect_to_server(SERVER_PATH)
        await client.chat_loop()
    finally:
        await client.exit_stack.aclose()

# Começo da interação com o usuário:
if __name__ == "__main__":
    valid_answers = ["carros", "car", "carro", "automóvel", "automovel", "veículos", "veiculos"]
    
    print("\nOlá, bem-vindo ao MCP Car")
    user_answer = input("Como posso lhe ajudar: ").lower()
    
    if any(word in user_answer for word in valid_answers):
        print("\nCaso queira pular algum dos filtros, basta digitar 'Não' ou apenas pressionar 'Enter'.")
        print("PS: Você pode digitar 'sair' para encerrar a conversa com nosso agente!\n")
        print("Entrando em contato com nosso agente...")
        asyncio.run(main())
    else:
        print("Não entendi sua resposta.")