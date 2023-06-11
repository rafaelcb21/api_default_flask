import unittest
import json
from flask_testing import TestCase
from main import app
from api.models.models import db, Produto
from api.config.config import configuration
from api.controllers.eventhub import enviar_json_ao_eventhub


class ApiTest(TestCase):
    def create_app(self):
        app.config.from_object(configuration["testing"])
        return app

    def setUp(self):
        try:
            db.create_all()
        except Exception as e:
            print("Erro: A conexão com o banco de dados não está aberta.", type(e).__name__)

    def test_database_connection(self):
        try:
            self.assertTrue(db.session.connection().closed == 0)
        except Exception as e:
            self.fail("Erro: A conexão com o banco de dados não está aberta.", type(e).__name__)

    def test_simulacao_endpoint(self):
        data = {"valorDesejado": 900.00, "prazo": 5}
        response = self.client.post("/simulacao/produto", json=data)
        self.assertEqual(response.status_code, 200)

    def test_simulacao_endpoint_method_get(self):
        response = self.client.get("/simulacao/produto")
        self.assertEqual(response.status_code, 405)

    def nao_retorna_produto(self, datas):
        contador = 0
        for data in datas:
            response = self.client.post("/simulacao/produto", json=data)
            response_data = json.loads(response.data.decode("utf-8"))

            if response_data["error"]["msg"] == "Produto nao encontrado":
                contador += 1

        return contador

    def retorna_produto(self, datas):
        resultado = []
        for data in datas:
            response = self.client.post("/simulacao/produto", json=data)
            response_data = json.loads(response.data.decode("utf-8"))
            produto = response_data["codigoProduto"]
            resultado.append({str(produto): data})

        return resultado

    def retorna_produto_schema_validar(self, datas):
        contador = 0
        for data in datas:
            response = self.client.post("/simulacao/produto", json=data)
            response_data = json.loads(response.data.decode("utf-8"))
            if list(response_data.keys()) == ['errors', 'message']:
                contador += 1

        return contador

    def test_estrutura_da_request(self):
        datas = [
            {"praz": 1, "valorDesejado": 200},
            {"prazo": "0r", "valorDesejado": 200}
        ]

        resultado = self.retorna_produto_schema_validar(datas)
        self.assertEqual(2, resultado)

    def test_simulacao_query(self):
        datas = [
            {"prazo": 1, "valorDesejado": 200},
            {"prazo": 1, "valorDesejado": 10000},
            {"prazo": 24, "valorDesejado": 200},
            {"prazo": 24, "valorDesejado": 10000},
            {"prazo": 25, "valorDesejado": 10000.01},
            {"prazo": 25, "valorDesejado": 100000.00},
            {"prazo": 48, "valorDesejado": 10000.01},
            {"prazo": 48, "valorDesejado": 100000.00},
            {"prazo": 49, "valorDesejado": 100000.01},
            {"prazo": 49, "valorDesejado": 1000000.00},
            {"prazo": 96, "valorDesejado": 100000.01},
            {"prazo": 96, "valorDesejado": 1000000.00},
            {"prazo": 97, "valorDesejado": 1000000.01},
            {"prazo": 97, "valorDesejado": 2000000.01},
            {"prazo": 100, "valorDesejado": 1000000.01},
            {"prazo": 100, "valorDesejado": 2000000.01}
        ]

        resultado = self.retorna_produto(datas)

        self.assertIn({"1": {"prazo": 1, "valorDesejado": 200}}, resultado)
        self.assertIn({"1": {"prazo": 1, "valorDesejado": 10000}}, resultado)
        self.assertIn({"1": {"prazo": 24, "valorDesejado": 200}}, resultado)
        self.assertIn({"1": {"prazo": 24, "valorDesejado": 10000}}, resultado)
        self.assertIn({"2": {"prazo": 25, "valorDesejado": 10000.01}}, resultado)
        self.assertIn({"2": {"prazo": 25, "valorDesejado": 100000.00}}, resultado)
        self.assertIn({"2": {"prazo": 48, "valorDesejado": 10000.01}}, resultado)
        self.assertIn({"2": {"prazo": 48, "valorDesejado": 100000.00}}, resultado)
        self.assertIn({"3": {"prazo": 49, "valorDesejado": 100000.01}}, resultado)
        self.assertIn({"3": {"prazo": 49, "valorDesejado": 1000000.00}}, resultado)
        self.assertIn({"3": {"prazo": 96, "valorDesejado": 100000.01}}, resultado)
        self.assertIn({"3": {"prazo": 96, "valorDesejado": 1000000.00}}, resultado)
        self.assertIn({"4": {"prazo": 97, "valorDesejado": 1000000.01}}, resultado)
        self.assertIn({"4": {"prazo": 97, "valorDesejado": 2000000.01}}, resultado)
        self.assertIn({"4": {"prazo": 100, "valorDesejado": 1000000.01}}, resultado)
        self.assertIn({"4": {"prazo": 100, "valorDesejado": 2000000.01}}, resultado)

    def test_produto_nao_encontrado(self):
        datas = [
            {"prazo": 25, "valorDesejado": 200},
            {"prazo": 1, "valorDesejado": 10000.01},
            {"prazo": 97, "valorDesejado": 10000.00},
            {"prazo": 49, "valorDesejado": 100000.00},
            {"prazo": -1, "valorDesejado": -200},
            {"prazo": -1, "valorDesejado": 200},
            {"prazo": 0, "valorDesejado": 200}
        ]

        resultado = self.nao_retorna_produto(datas)

        self.assertEqual(resultado, 7)

    def test_produto_columns(self):
        columns = Produto.__table__.columns.keys()

        self.assertIn("co_produto", columns)
        self.assertIn("no_produto", columns)
        self.assertIn("pc_taxa_juros", columns)
        self.assertIn("nu_minimo_meses", columns)
        self.assertIn("nu_maximo_meses", columns)
        self.assertIn("vr_minimo", columns)
        self.assertIn("vr_maximo", columns)

        self.assertEqual(str(Produto().__table__.c.co_produto.type), "INTEGER")
        self.assertEqual(str(Produto().__table__.c.no_produto.type), "VARCHAR(200)")
        self.assertEqual(
            str(Produto().__table__.c.pc_taxa_juros.type), "NUMERIC(10, 9)"
        )
        self.assertEqual(str(Produto().__table__.c.nu_minimo_meses.type), "SMALLINT")
        self.assertEqual(str(Produto().__table__.c.nu_maximo_meses.type), "SMALLINT")
        self.assertEqual(str(Produto().__table__.c.vr_minimo.type), "NUMERIC(18, 2)")
        self.assertEqual(str(Produto().__table__.c.vr_maximo.type), "NUMERIC(18, 2)")

        self.assertTrue(len(columns) == 7)

    def test_eventhub_connection(self):
        eventhub = enviar_json_ao_eventhub({"id": 1, "msg": "flask_test"})
        self.assertEqual(eventhub, "ok")


if __name__ == "__main__":
    unittest.main()
