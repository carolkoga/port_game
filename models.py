from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Desafio(db.Model):
    __tablename__ = 'desafios'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_porta = db.Column(db.Integer, nullable=False, unique=True)
    sigla = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    eh_segura = db.Column(db.Boolean, default=True)
    categoria = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "porta": self.numero_porta,
            "sigla": self.sigla,
            "descricao": self.descricao,
            "segura": self.eh_segura,
            "categoria": self.categoria
        }