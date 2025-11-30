class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://usuario:senha@localhost:5432/meubanco"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
