ENVIRONMENT = 'development'

class Config:
    CURRENT_LANGUAGE = "zh"
    TBK_NODE_NAME = "TBK-Client"
    FONT_FILE = "static/font/BLACK-NORMAL.ttf"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


configurations = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

config = configurations[ENVIRONMENT]