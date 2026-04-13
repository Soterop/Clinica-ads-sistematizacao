from flask import render_template, request, redirect, url_for, flash
from app import app, db

# Modelo do Banco de Dados
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    profissional = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(10), nullable=False)

# Mock de Profissionais
PROFISSIONAIS = [
    {"id": 1, "imagem": "paulo.png","nome": "Dr. Paulo", "especialidade": "Cardiologia", "planos": ["Unimed", "Bradesco"]},
    {"id": 2, "imagem": "joana.png","nome": "Dra. Joana", "especialidade": "Dermatologia", "planos": ["Amil", "Particular"]},
    {"id": 3, "imagem": "andre.png", "nome": "Dr. André", "especialidade": "Ortopedia", "planos": ["Unimed", "Casssi", "Particular"]},
]

# Cria o banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', profissionais=PROFISSIONAIS)

@app.route('/agendar', methods=['POST'])
def agendar():
    try:
        raw_cpf = request.form.get('cpf')
        if not raw_cpf:
            flash("CPF é obrigatório")
            return redirect(url_for('index'))
            
        cpf_limpo = ''.join(filter(str.isdigit, raw_cpf))
        
        prof_id_raw = request.form.get('profissional')
        if not prof_id_raw:
            flash("Selecione um profissional")
            return redirect(url_for('index'))
            
        prof_id = int(prof_id_raw)
        prof = next((p for p in PROFISSIONAIS if p['id'] == prof_id), None)

        novo = Agendamento(
            nome=request.form.get('nome'),
            cpf=cpf_limpo,
            profissional=prof['nome'],
            especialidade=prof['especialidade'],
            data=request.form.get('data'),
            horario=request.form.get('horario')
        )
        
        db.session.add(novo)
        db.session.commit()
        flash('Agendamento realizado com sucesso!')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao agendar. Tente novamente.')

    return redirect(url_for('index'))

@app.route('/lista')
def lista_agendamentos():
    todos = Agendamento.query.all()
    # CORREÇÃO: Adicionado .html
    return render_template('lista.html', agendamentos=todos)

@app.route('/cancelar/<int:id_agendamento>', methods=['POST'])
def cancelar(id_agendamento):
    agendamento = Agendamento.query.get_or_404(id_agendamento)
    try:
        db.session.delete(agendamento)
        db.session.commit()
        flash('Agendamento removido com sucesso!')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao cancelar agendamento.')
    
    return redirect(url_for('lista_agendamentos'))