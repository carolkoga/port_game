import os
from flask import Flask 
from models import db, Desafio
from dotenv import load_dotenv

load_dotenv()

def create_db():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas no Neon com sucesso!")
        if not Desafio.query.filter_by(numero_porta=22).first():
            teste = Desafio(
                numero_porta=22, 
                sigla="SSH", 
                descricao="Secure Shell - Acesso remoto seguro", 
                eh_segura=True,
                categoria="Infra"
            )
            db.session.add(teste)
            db.session.commit()
            print("🚀 Desafio de teste (Porta 22) inserido!")

if __name__ =="__main__":
    create_db()