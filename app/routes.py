from flask import render_template, request, redirect, url_for, flash
from app import app, db


class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    profissional = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(10), nullable=False)


PROFISSIONAIS = [
    {"id": 1, "imagem": "paulo.png","nome": "Dr. Paulo", "especialidade": "Cardiologia", "planos": ["Unimed", "Bradesco"]},
    {"id": 2, "imagem": "joana.png","nome": "Dra. Joana", "especialidade": "Dermatologia", "planos": ["Amil", "Particular"]},
    {"id": 3, "imagem": "andre.png", "nome": "Dr. André", "especialidade": "Ortopedia", "planos": ["Unimed", "Casssi", "Particular"]},
]


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', profissionais=PROFISSIONAIS)

@app.route('/agendar', methods=['POST'])
def agendar():
    try:
  
        raw_cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        data_escolhida = request.form.get('data')
        hora_escolhida = request.form.get('horario')
        prof_id_raw = request.form.get('profissional')

        if not raw_cpf or not prof_id_raw:
            flash("Preencha todos os campos obrigatórios!")
            return redirect(url_for('index'))
            
        cpf_limpo = ''.join(filter(str.isdigit, raw_cpf))
        
       
        prof_id = int(prof_id_raw)
        prof = next((p for p in PROFISSIONAIS if p['id'] == prof_id), None)
        
        if not prof:
            flash("Profissional não encontrado.")
            return redirect(url_for('index'))

        
        conflito = Agendamento.query.filter_by(
            data=data_escolhida, 
            horario=hora_escolhida, 
            profissional=prof['nome']
        ).first()

        if conflito:
            flash(f"Atenção: O {prof['nome']} já possui um agendamento para este dia e horário!")
            return redirect(url_for('index'))
     

       
        novo = Agendamento(
            nome=nome,
            cpf=cpf_limpo,
            profissional=prof['nome'],
            especialidade=prof['especialidade'],
            data=data_escolhida,
            horario=hora_escolhida
        )
        
        db.session.add(novo)
        db.session.commit()
        flash('Agendamento realizado com sucesso!')
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro: {e}") 
        flash('Erro ao agendar. Tente novamente.')

    return redirect(url_for('index'))

@app.route('/lista')
def lista_agendamentos():
   
    filtro_cpf = request.args.get('cpf')
    filtro_prof = request.args.get('profissional')
    filtro_data = request.args.get('data')

  
    query = Agendamento.query

   
    if filtro_cpf:
        
        cpf_busca = ''.join(filter(str.isdigit, filtro_cpf))
        if cpf_busca:
            query = query.filter(Agendamento.cpf == cpf_busca)
    
    if filtro_prof:
        query = query.filter(Agendamento.profissional == filtro_prof)
        
    if filtro_data:
        
        query = query.filter(Agendamento.data == filtro_data)

    
    agendamentos_filtrados = query.order_by(Agendamento.data.asc()).all()

   
    nomes_profissionais = [p['nome'] for p in PROFISSIONAIS]

   
    return render_template('lista.html', 
                           agendamentos=agendamentos_filtrados, 
                           profissionais_lista=nomes_profissionais)



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