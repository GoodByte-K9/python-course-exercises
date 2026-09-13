from dotenv import load_dotenv
import os

from extensions import app, db, login_manager
import routes

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI", "sqlite:///posts.db")

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=False, port=5002)
