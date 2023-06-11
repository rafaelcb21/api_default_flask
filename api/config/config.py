import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DB = os.environ.get("DB")
    PORT = os.environ.get("PORT")
    LOGIN = os.environ.get("LOGIN")
    PASSWORD = os.environ.get("PASSWORD")
    EVENTHUB_NAME = os.environ.get("EVENTHUB_NAME")
    EVENTHUB_ENDPOINT = os.environ.get("EVENTHUB_ENDPOINT")
    SWAGGER_MASK_SWAGGER = os.environ.get("SWAGGER_MASK_SWAGGER")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://{}:{}@{}:{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
            Config.LOGIN, Config.PASSWORD, Config.DATABASE_URL, Config.PORT, Config.DB
        )
    )
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://{}:{}@{}:{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
            Config.LOGIN, Config.PASSWORD, Config.DATABASE_URL, Config.PORT, Config.DB
        )
    )
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


configuration = {
    "base": Config,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
