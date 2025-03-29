import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from pathlib import Path

ROOT_PATH =  Path(__file__).parent.parent
SERVER_PATH = str(ROOT_PATH / 'app/server.py')

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_teste: str):
        """Connect to an MCP server"""
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

        # List available tools
        # response = await self.session.list_tools()
        # tools = response.tools

    async def process_query(self, query):
        """Envia a consulta para o servidor MCP e retorna a resposta."""

        if not self.session:
            return "Erro: Cliente não conectado ao servidor."

        # Listar as ferramentas disponíveis no servidor
        # response = await self.session.list_tools()
        # tools = {tool.name for tool in response.tools}  # Converte para um conjunto de strings
        result = await self.session.call_tool("fetch_data", {"filters": query})
        # print(query, '\n', result)
        return result.content[0].text
        

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nRodando o MCP client")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = {}
                query["color"] = input("\ncolor: ")
                query["transmission"] = input("\ntransmission: ")
                query["brand"] = input("\nbrand")

                # if query.lower() == 'quit':
                #     break
                
                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

async def main():
    client = MCPClient()
    await client.connect_to_server(SERVER_PATH)
    await client.chat_loop()

if __name__ == "__main__":
    asyncio.run(main())