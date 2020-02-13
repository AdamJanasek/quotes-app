import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_flask_cfg():
    env_flask_config = os.environ.get("FLASK_ENV")

    if env_flask_config == "production":
        return ProductionConfig()

    elif env_flask_config == "testing":
        return TestingConfig()

    else:
        return DevelopmentConfig()


flask_name = os.environ.get("FLASK_APP")
flask_config = get_flask_cfg()
