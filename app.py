from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from models import db, Registro
import os
import re
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import io

app = Flask(__name__)

# Caminho absoluto para o banco de dados dentro da pasta 'instance'
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db.init_app(app)

# ------------------- FUNÇÕES DE VALIDAÇÃO -------------------


def validar_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '').strip()
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    return resto == int(cpf[10])


def validar_placa(placa):
    placa = placa.upper().strip()
    regex_mercosul = re.compile(r'^[A-Z]{3}-?\d[A-Z]{1}\d{2}$')
    regex_nacional = re.compile(r'^[A-Z]{3}-?\d{4}$')
    return bool(regex_mercosul.match(placa) or regex_nacional.match(placa))

# ------------------- LOGIN -------------------


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if usuario == 'admin' and senha == '1234,sh':
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------- INDEX -------------------


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    today_date = date.today().isoformat()
    form_data = {
        'data': today_date,
        'hora_entrada': '',
        'fornecedor': '',
        'nome_motorista': '',
        'cpf': '',
        'placa': '',
        'hora_saida': '',
        'observacao': ''
    }

    if request.method == 'POST':
        for campo in form_data:
            form_data[campo] = request.form.get(campo, '').strip()

        required_fields = {
            'data': 'Data',
            'hora_entrada': 'Hora Entrada',
            'fornecedor': 'Fornecedor',
            'nome_motorista': 'Nome do Motorista',
            'cpf': 'CPF',
            'placa': 'Placa Caminhão'
        }

        for field, name in required_fields.items():
            if not form_data[field]:
                flash(f'O campo "{name}" é obrigatório.', 'danger')
                return render_template('index.html', **form_data, today=today_date)

        if not validar_cpf(form_data['cpf']):
            flash('CPF inválido.', 'danger')
            return render_template('index.html', **form_data, today=today_date)

        if not validar_placa(form_data['placa']):
            flash('Placa inválida.', 'danger')
            return render_template('index.html', **form_data, today=today_date)

        novo_registro = Registro(**form_data)
        try:
            db.session.add(novo_registro)
            db.session.commit()
            flash('Registro salvo com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar registro: {e}', 'danger')

    return render_template('index.html', **form_data, today=today_date)

# ------------------- REGISTROS -------------------


@app.route('/registros', methods=['GET', 'POST'])
def registros():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    hoje = datetime.today().strftime('%Y-%m-%d')
    data_inicio = request.args.get(
        'data_inicio') or session.get('data_inicio') or hoje
    data_fim = request.args.get('data_fim') or session.get('data_fim') or hoje
    session['data_inicio'] = data_inicio
    session['data_fim'] = data_fim

    registros = Registro.query.filter(
        Registro.data >= data_inicio,
        Registro.data <= data_fim
    ).order_by(Registro.data.asc()).all()

    return render_template('registros.html', registros=registros,
                           data_inicio=data_inicio, data_fim=data_fim)

# ------------------- PDF -------------------


@app.route('/download_pdf')
def download_pdf():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    query = Registro.query
    if data_inicio:
        query = query.filter(Registro.data >= data_inicio)
    if data_fim:
        query = query.filter(Registro.data <= data_fim)

    registros = query.order_by(Registro.data.asc()).all()
    pdf_buffer = gerar_pdf(registros)
    return send_file(pdf_buffer, as_attachment=True,
                     download_name="registros_acesso_fornecedor.pdf",
                     mimetype='application/pdf')


def gerar_pdf(registros):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(A4[1], A4[0]))
    elements = [Paragraph("Controle Acesso Recebimento Fornecedor",
                          getSampleStyleSheet()['Title']), Spacer(1, 12)]

    data = [['Data', 'Hora Entrada', 'Fornecedor', 'Nome Motorista',
             'CPF', 'Placa Caminhão', 'Hora Saída', 'Observação']]
    for r in registros:
        data.append([r.data, r.hora_entrada, r.fornecedor, r.nome_motorista,
                     r.cpf, r.placa, r.hora_saida, r.observacao])

    tabela = Table(data)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(tabela)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ------------------- EDITAR/EXCLUIR -------------------


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    registro = Registro.query.get_or_404(id)
    if request.method == 'POST':
        registro.hora_saida = request.form['hora_saida']
        db.session.commit()
        flash('Hora de saída atualizada!', 'success')
        return redirect(url_for('registros'))

    return render_template('editar.html', registro=registro)


@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    registro = Registro.query.get_or_404(id)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('Registro excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir registro: {e}', 'danger')
    return redirect(url_for('registros'))

# ------------------- EXECUTAR -------------------


if __name__ == '__main__':
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with app.app_context():
            db.create_all()
    app.run(debug=True)


# if __name__ == '__main__':
#     if not os.path.exists(db_path):
#         os.makedirs(os.path.dirname(db_path), exist_ok=True)
#         with app.app_context():
#             db.create_all()


#     app.run(host='0.0.0.0', port=5000, debug=True)
