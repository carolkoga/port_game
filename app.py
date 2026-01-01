import os
from flask import Flask, render_template, request, jsonify, session
from models import db, Desafio
from dotenv import load_dotenv
from sqlalchemy.sql.expression import func

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("'SECRET_KEY", 'cyber-koga-secret')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
    return render_template('index.html', score=session['score'])

@app.route('/get_challenge', methods=['GET'])
def get_challenge():
    desafio = Desafio.query.order_by(func.random()).first()
    if desafio:
        return jsonify(desafio.to_dict())
    return jsonify({"error": "Nenhum desafio encontrado"}), 404

@app.route('/check_answer',methods=['POST'])
def check_answer():
    data = request.json
    desafio_id = data.get('id')
    user_sigla = data.get('sigla', '').strip().upper()

    desafio = Desafio.query.get(desafio_id)

    if desafio and desafio.sigla.upper() == user_sigla:
        session['score'] == 10
        return jsonify({
            "correct": True,
            "message": "Correto! +10 pontos.",
            "new_score": session['score'],
            "details": dasefio.to_dict()
        })

    else: 
        return jsonify({
            "correct": False, 
            "message": f"Incorreto. A sigla correta era {desafio.sigla}",
            "new_score": session['score']
        })

if __name__ == "__main__":
    app.run(debug=True)