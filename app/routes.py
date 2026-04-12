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
    horario = db.Column(db.String(10), nullable=False) # <--- Novo campo

# Mock de Profissionais (mantemos para o formulário)
PROFISSIONAIS = [
    {"id": 1, "imagem": "paulo.png","nome": "Dr. Paulo", "especialidade": "Cardiologia", "planos": ["Unimed", "Bradesco"]},
    {"id": 2, "imagem": "joana.png","nome": "Dra. Joana", "especialidade": "Dermatologia", "planos": ["Amil", "Particular"]},
    {"id": 3, "imagem": "andre.png", "nome": "Dr. André", "especialidade": "Ortopedia", "planos": ["Unimed", "Casssi", "Particular"]},
]

# Cria o banco de dados na primeira execução
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', profissionais=PROFISSIONAIS)

@app.route('/agendar', methods=['POST'])
def agendar():
    try:
        # 1. Limpeza do CPF
        raw_cpf = request.form.get('cpf')
        if not raw_cpf:
            flash("CPF é obrigatório")
            return redirect(url_for('index'))
            
        cpf_limpo = ''.join(filter(str.isdigit, raw_cpf))
        
        # 2. Busca do Profissional (O erro pode estar aqui!)
        prof_id_raw = request.form.get('profissional')
        if not prof_id_raw:
            flash("Selecione um profissional")
            return redirect(url_for('index'))
            
        prof_id = int(prof_id_raw)
        prof = next((p for p in PROFISSIONAIS if p['id'] == prof_id), None)

        # 3. Criação e Salvamento
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
        
        print("DEBUG: Agendamento salvo com sucesso!") # Veja isso no terminal
        flash('Agendamento realizado com sucesso!')
        
    except Exception as e:
        print(f"DEBUG ERRO: {e}") # Isso vai te dizer exatamente o que quebrou
        db.session.rollback()
        flash('Erro ao agendar. Tente novamente.')

    return redirect(url_for('index'))

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    raw_cpf = request.form.get('cpf')
    cpf_limpo = ''.join(filter(str.isdigit, raw_cpf))
    agendamentos = []
    cpf_busca = ""
    if request.method == 'POST':
        cpf_busca = request.form.get('cpf')
        agendamentos = Agendamento.query.filter_by(cpf=cpf_busca).all()
    return render_template('consultar.html', agendamentos=agendamentos, cpf=cpf_busca)


@app.route('/lista')
def lista_agendamentos():
    # Busca TODOS os agendamentos do banco sem filtro
    todos = Agendamento.query.all()
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
    
    # Redireciona para a lista para você ver que sumiu
    return redirect(url_for('lista_agendamentos'))
