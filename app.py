import os
from flask import Flask, render_template, request, jsonify, session
from models import db, Desafio
from dotenv import load_dotenv
from sqlalchemy.sql.expression import func

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'cyber-koga-secret')

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
    return render_template('index.html', score=session['score'])

@app.route('/get_challenge', methods=['GET'])
def get_challenge():
    try:
        desafio = Desafio.query.order_by(func.random()).first()
        if desafio:
            return jsonify(desafio.to_dict())
        return jsonify({"error": "Banco de dados vazio ou erro de conexão"}), 404
    except Exception as e:
        print(f"ERRO DE BANCO: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    desafio_id = data.get('id')
    user_sigla = data.get('sigla', '').strip().upper()

    desafio = db.session.get(Desafio, desafio_id)

    if not desafio:
        return jsonify({"error": "Desafio não encontrado"}), 404

    if desafio.sigla.upper() == user_sigla:
        session['score'] += 10
        return jsonify({
            "correct": True,
            "message": "ACCESS GRANTED! Sigla correta.",
            "new_score": session['score'],
            "details": desafio.to_dict()
        })
    else: 
        return jsonify({
            "correct": False, 
            "message": f"ACCESS DENIED! A sigla correta era {desafio.sigla}.",
            "new_score": session['score'],
            "details": desafio.to_dict()
        })

if __name__ == "__main__":
    app.run(debug=True)