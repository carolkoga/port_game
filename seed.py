import os
from flask import Flask 
from models import db, Desafio
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        portas_cyber = [
            # --- Acesso Remoto & Transferência ---
            {"num": 20, "sig": "FTP-DATA", "desc": "Canal de dados do FTP. Texto claro (Inseguro).", "seg": False, "cat": "Arquivos"},
            {"num": 21, "sig": "FTP", "desc": "Canal de controle do FTP. Envia senhas em texto claro. Vetor de Sniffing.", "seg": False, "cat": "Arquivos"},
            {"num": 22, "sig": "SSH", "desc": "Secure Shell. Padrão para administração remota criptografada. Substitui Telnet.", "seg": True, "cat": "Acesso"},
            {"num": 23, "sig": "Telnet", "desc": "Acesso remoto legado. Texto claro. Se aberta, é falha grave de segurança.", "seg": False, "cat": "Acesso"},
            {"num": 69, "sig": "TFTP", "desc": "Trivial FTP (UDP). Sem autenticação. Usado em boot de rede. Perigoso se exposto.", "seg": False, "cat": "Arquivos"},
            
            # --- Web ---
            {"num": 80, "sig": "HTTP", "desc": "Web padrão. Sem criptografia. Vulnerável a Man-in-the-Middle.", "seg": False, "cat": "Web"},
            {"num": 443, "sig": "HTTPS", "desc": "Web segura com TLS/SSL. Garante confidencialidade e integridade.", "seg": True, "cat": "Web"},
            {"num": 8080, "sig": "HTTP-Proxy", "desc": "Alternativa comum para servidores web ou proxies. Geralmente sem HTTPS por padrão.", "seg": False, "cat": "Web"},

            # --- E-mail (Importante saber a diferença!) ---
            {"num": 25, "sig": "SMTP", "desc": "Envio de e-mail entre servidores. Frequentemente abusado para SPAM/Relay.", "seg": False, "cat": "E-mail"},
            {"num": 110, "sig": "POP3", "desc": "Recebimento de e-mail (baixa e apaga). Texto claro.", "seg": False, "cat": "E-mail"},
            {"num": 143, "sig": "IMAP", "desc": "Recebimento de e-mail (sincroniza). Texto claro.", "seg": False, "cat": "E-mail"},
            {"num": 465, "sig": "SMTPS", "desc": "SMTP seguro (SSL/TLS implícito).", "seg": True, "cat": "E-mail"},
            {"num": 587, "sig": "SMTP-SUB", "desc": "SMTP Submission. Padrão moderno seguro com STARTTLS.", "seg": True, "cat": "E-mail"},
            {"num": 993, "sig": "IMAPS", "desc": "IMAP sobre SSL/TLS. Padrão seguro para leitura de e-mails.", "seg": True, "cat": "E-mail"},
            {"num": 995, "sig": "POP3S", "desc": "POP3 sobre SSL/TLS.", "seg": True, "cat": "E-mail"},

            # --- Infraestrutura & Windows (Alvos Comuns) ---
            {"num": 53, "sig": "DNS", "desc": "Resolução de nomes. UDP (Consultas) e TCP (Transferência de Zona - Reconhecimento).", "seg": True, "cat": "Infra"},
            {"num": 88, "sig": "Kerberos", "desc": "Autenticação centralizada (Active Directory). Alvo de ataques 'Golden Ticket'.", "seg": True, "cat": "Auth"},
            {"num": 137, "sig": "NetBIOS", "desc": "Serviço de nomes Windows antigo. Frequentemente explorado para enumeração.", "seg": False, "cat": "Windows"},
            {"num": 139, "sig": "NetBIOS-SSN", "desc": "Sessão NetBIOS. Vulnerável a enumeração de usuários.", "seg": False, "cat": "Windows"},
            {"num": 445, "sig": "SMB", "desc": "Compartilhamento de arquivos Windows. Alvo crítico (ex: WannaCry/EternalBlue).", "seg": False, "cat": "Windows"},
            {"num": 389, "sig": "LDAP", "desc": "Lightweight Directory Access Protocol. Texto claro. Enumeração de diretório.", "seg": False, "cat": "Auth"},
            {"num": 636, "sig": "LDAPS", "desc": "LDAP sobre SSL. Versão segura para consultas de diretório.", "seg": True, "cat": "Auth"},
            {"num": 3389, "sig": "RDP", "desc": "Remote Desktop. Alvo #1 de Ransomware via força bruta.", "seg": False, "cat": "Windows"},

            # --- Bancos de Dados (Se expostos, é problema) ---
            {"num": 1433, "sig": "MSSQL", "desc": "SQL Server da Microsoft. Alvo de injeção SQL e força bruta.", "seg": True, "cat": "Banco de Dados"},
            {"num": 1521, "sig": "Oracle", "desc": "Oracle Database. TNS Listener. Alvo comum em corporações.", "seg": True, "cat": "Banco de Dados"},
            {"num": 3306, "sig": "MySQL", "desc": "MySQL/MariaDB. Nunca deve estar exposta publicamente.", "seg": True, "cat": "Banco de Dados"},
            {"num": 5432, "sig": "PostgreSQL", "desc": "Postgres. Porta padrão do nosso banco Neon!", "seg": True, "cat": "Banco de Dados"},
            {"num": 6379, "sig": "Redis", "desc": "Banco NoSQL em memória. Frequentemente encontrado sem senha (inseguro).", "seg": False, "cat": "Banco de Dados"},
            {"num": 27017, "sig": "MongoDB", "desc": "Banco NoSQL. Famoso por configurações padrão sem autenticação no passado.", "seg": False, "cat": "Banco de Dados"},

            # --- Gerenciamento ---
            {"num": 161, "sig": "SNMP", "desc": "Monitoramento de rede (UDP). Versões 1 e 2c enviam 'community strings' em texto claro.", "seg": False, "cat": "Infra"},
            {"num": 514, "sig": "Syslog", "desc": "Logs do sistema (UDP). Texto claro. Atacantes podem ler logs de segurança.", "seg": False, "cat": "Logs"},
            {"num": 5900, "sig": "VNC", "desc": "Virtual Network Computing. Acesso remoto gráfico. Frequentemente inseguro.", "seg": False, "cat": "Acesso"}
        ]

        print(f"🔄 Preparando para inserir/atualizar {len(portas_cyber)} portas no Neon...")
        
        count_add = 0

        for p in portas_cyber:
            existente = Desafio.query.filter_by(numero_porta=p["num"]).first()

            if not existente:
                novo = Desafio(
                    numero_porta=p["num"],
                    sigla=p["sig"],
                    descricao=p["desc"],
                    eh_segura=p["seg"],
                    categoria=p["cat"]
                )
                db.session.add(novo)
                count_add += 1

        db.session.commit()
        print(f"✅ Sucesso! {count_add} novas portas adicionadas ao banco de dados.")
        print("🎉 Etapa de Banco de Dados CONCLUÍDA!")

if __name__ == "__main__":
    seed_database()