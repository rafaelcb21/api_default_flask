import os
from api import create_app
from api.models.models import db
import unittest


__version__ = '1.0.0'


app = create_app(config_name="development")
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Erro: A conexão com o banco de dados não está aberta.", repr(e))


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False)
