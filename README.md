# SIMULACAO API

Este projeto é um simulador de empréstimos/financiamento, no qual o cliente envia para a API o `prazo` em meses que deseja pagar esse financiamento, e envia o `valorDesejado` desse financiamento.

A API irá retornar o valor das parcelas na tabela PRICE e na tabela SAC, e antes de enviar a resposta ao cliente existem diversas validações na API, mantendo assim a qualidade da resposta.

O projeto contêm logs, testes de integração, testes unitários e um documentação em Swagger da API.

A API foi construida em python usando o framework Flask e Flask-RestX. Todo o projeto está modularizado em blueprints permitindo inserir outras rotas e até outras APIs no mesmo projeto.

As configurações encontram-se no arquivo .env, é utilizado uma conexão com o SQLServer para buscar o produto especifico ao emprestimo desejado pelo cliente, e cada resposta da API é enviada também ao EventHub para analise estatísticas de outros departamentos.

## Pré-requisitos

Certifique-se de ter o [Python 3](https://www.python.org/downloads/)  instalado na sua máquina. 

Instale o driver do SQLServer versão 17 [`download`](https://go.microsoft.com/fwlink/?linkid=2223304) ele se encontra no seguinte [endereço](https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows) juntamente com outras versões.

Após fazer o download do arquivo `msodbcsql.msi` basta executa-lo para instalar o drive.

Consulte o site da [Microsoft](https://learn.microsoft.com/pt-br/sql/connect/odbc/windows/system-requirements-installation-and-driver-files?view=sql-server-ver16#installing-microsoft-odbc-driver-for-sql-server) para mais informações.

## Instalação
Dentro da pasta raiz do projeto:
1. Crie o ambiente virtual:
```bash
python.exe -m venv meu_venv
``` 
Irá aparecer no inicio da linha de comando a seguinte informação `(meu_venv)`

2.  Instale todas as dependências do projeto no ambiente virtual:
```bash
pip install -r requirements.txt
```
3.  Configure o ambiente virtual para utilizar o Flask executando o seguinte comando:
```bash
set FLASK_APP=main
```
4. Execute os testes para verificar que esta tudo funcionando com o comando:
```bash
flask test
```
Aparecendo `OK` no final significa que esta tudo funcionando.

5. Inicialize a aplicação com o comando:
```bash
flask run
```
6. No vscode (Visual Studio Code) instale a extençao `REST Client` para poder fazer testes no arquivo `test_api.http` diretamente no vscode.
  
7. No localhost o projeto funciona na porta 5000 `http://127.0.0.1:5000`
  
8. A documentação do projeto esta no formato `swagger` e para verificar e interagir com a API, com a aplicação rodando entre no seguinte endereço `http://127.0.0.1:5000/swagger`