from flask import Blueprint
from sqlalchemy.sql.expression import func
from ..models.models import Produto
from ..controllers.financiamento import tabela_price, tabela_sac
from ..controllers.eventhub import enviar_json_ao_eventhub
from flask import current_app

from log.log_config import logger
from flask_restx import Namespace, Resource, fields, reqparse, abort


# Construcao do Namespace Simulacao
simulacao_ns = Namespace('simulacao', 'Simulador API endpoints')

# Criando o modelo de request da api para o namespace Simulacao
simulacao_request_model = simulacao_ns.model('SimulacaoRequest', {
    'prazo': fields.Integer(
        required=True,
        description='Prazo do emprestimo'
    ),
    'valorDesejado': fields.Float(
        required=True,
        description='Valor desejado no emprestimo'
    )
})

# Criando o modelo de resposta, referente a Parcela
parcela_model = simulacao_ns.model('Parcela', {
    'numero': fields.Integer(
        readonly=True,
        description='Número da parcela'
    ),
    'valorAmortizacao': fields.Float(
        readonly=True,
        description='Valor de amortização da parcela'
    ),
    'valorJuros': fields.Float(
        readonly=True,
        description='Valor de juros da parcela'
    ),
    'valorPrestacao': fields.Float(
        readonly=True,
        description='Valor total da prestação da parcela'
    )
})

# Criando o modelo de resposta, referente ao Tipo, que engloba o modelo Parcela
tipo_modelo = simulacao_ns.model('Tipo', {
    'tipo': fields.String(
        readonly=True,
        description='Tipo da tabela de financiamento'
    ),
    'parcelas': fields.List(
        fields.Nested(parcela_model),
        readonly=True,
        description='Lista de parcelas'
    )
})

# Criando o modelo final da resposta, que engloba o modelo Tipo
simulacao_response_model = simulacao_ns.model('SimulacaoResponse', {
    'codigoProduto': fields.Integer(
        readonly=True,
        description='Código do produto'
    ),
    'descricaoProduto': fields.String(
        readonly=True,
        description='Descrição do produto'
    ),
    'taxaJuros': fields.Float(
        readonly=True,
        description='Taxa de juros'
    ),
    'resultadoSimulacao': fields.List(
        fields.Nested(tipo_modelo),
        readonly=True,
        description='Lista de tipos de financiamento'
    )
})

# Criando o modelo de resposta para o erro
erro_modelo = simulacao_ns.model('Erro', {
    'msg': fields.String(
        readonly=True,
        description='Bad Request'
    )
})

simulacao = Blueprint("main", __name__)

simulacao_request_parser = reqparse.RequestParser()
simulacao_request_parser.add_argument('prazo', type=int, required=True, help='Prazo do emprestimo')
simulacao_request_parser.add_argument('valorDesejado', type=float, required=True, help='Valor desejado no emprestimo')


@simulacao_ns.route("/produto", methods=["POST"])
class Simulacao(Resource):

    @simulacao_ns.doc('Endpoint da Simulacao')
    @simulacao_ns.expect(simulacao_request_model)
    @simulacao_ns.marshal_with(simulacao_response_model)
    def post(self):

        data = simulacao_request_parser.parse_args()

        valor = data["valorDesejado"]
        prazo = data["prazo"]

        if int(prazo) == 0:
            abort(404, error={'msg': 'Produto nao encontrado'})

        valor_maximo_tratado = func.coalesce(Produto.vr_maximo, 1000000000000)
        prazo_maximo_tratado = func.coalesce(Produto.nu_maximo_meses, 1000000000000)

        produto = Produto.query.filter(
            Produto.vr_minimo <= valor,
            valor_maximo_tratado >= valor,
            Produto.nu_minimo_meses <= prazo,
            prazo_maximo_tratado >= prazo,
        ).first()

        if produto:
            tb_price = tabela_price(valor, prazo, produto.pc_taxa_juros)
            tb_sac = tabela_sac(valor, prazo, produto.pc_taxa_juros)

            data_dict = {
                "codigoProduto": produto.co_produto,
                "descricaoProduto": produto.no_produto,
                "taxaJuros": float(produto.pc_taxa_juros),
                "resultadoSimulacao": [
                    {"tipo": "SAC", "parcelas": tb_sac},
                    {"tipo": "PRICE", "parcelas": tb_price},
                ],
            }

            if current_app.config["TESTING"] is False:
                enviar_json_ao_eventhub(data_dict)

            return data_dict, 200

        logger.error({'msg': 'Produto nao encontrado'})
        abort(404, error={'msg': 'Produto nao encontrado'})
