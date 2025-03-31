# Projeto MCP

Este é um projeto finalizado que utiliza o protocolo MCP (Model Context Protocol) para comunicação entre cliente e servidor. O projeto inclui a criação de um banco de dados SQLite e a implementação de um cliente que consulta esse banco.

### Estrutura de pastas

📁 mcp-car   
│-- 📂 app  
│   ├── server.py  # Arquivo do servidor MCP   
│   ├── database.py  # Script responsável pela criaçãodo banco de dados  
│-- 📂 client  
│   ├── client.py  # Código principal do cliente onde ocorre interação  
│-- 📂 utils  
│   ├── create_cars.py  # Gera dados fictícios de carros e para o banco de dados
│-- README.md  # Documentação do projeto

### Como rodar o projeto

1. **Criar o banco de dados**
   - Navegue até a pasta `app`.
   - Abra o arquivo `database.py` e execute-o para criar o banco de dados no formato SQLite. Este script criará a estrutura necessária para armazenar os dados dos carros.

2. **Preencher o banco de dados com dados fictícios**
   - Acesse a pasta `utils`.
   - Abra o arquivo `create_cars.py` e execute-o para popular o banco de dados com 100 registros de carros fictícios. Esse passo é necessário para ter dados no banco antes de rodar o sistema.

3. **Executar o cliente e consultar os dados**
   - Com o banco de dados preenchido, vá até a pasta `client`.
   - Execute o arquivo `client.py` para interagir com o sistema. O agente permitirá que você insira filtros (como marca, modelo, ano, etc.) para procurar carros no banco de dados.

### Exemplo de uso

Ao rodar o cliente (`client.py`), você será solicitado a informar critérios de busca, como:

- Marca
- Modelo
- Ano
- Cor
- Preço máximo

O cliente enviará a consulta para o servidor, que realizará a busca no banco de dados e retornará os carros que atendem aos critérios fornecidos.

Você pode interromper a busca digitando **"sair"** a qualquer momento.

---

## Contribuições

Sinta-se à vontade para explorar e modificar o projeto conforme necessário. Caso tenha dúvidas ou queira sugerir melhorias, envie um pull request ou entre em contato.