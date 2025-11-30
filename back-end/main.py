from app import create_app, db
from app.routes import api

app = create_app()

app.register_blueprint(api)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
