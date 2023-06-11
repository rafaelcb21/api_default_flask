from flask import Flask, jsonify
from api.config.config import configuration
from api.routes.simulacao import simulacao, simulacao_ns
from .models.models import db
from flask_restx import Api


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configuration[config_name])
    app.config['SWAGGER_MASK_SWAGGER'] = False
    db.init_app(app)

    api = Api(
        simulacao,
        title='API Simulador',
        version='1.0',
        description='Documentacao da API de simulacao de emprestimo',
        doc='/swagger'
    )

    api.add_namespace(simulacao_ns)

    app.register_blueprint(simulacao)

    @app.errorhandler(404)
    def not_found_error(error):
        response = {"error": "Pagina nao encontrada", "status": 404}
        return jsonify(response), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        response = {"error": "Metodo nao permitido", "status": 405}
        return jsonify(response), 405

    return app
