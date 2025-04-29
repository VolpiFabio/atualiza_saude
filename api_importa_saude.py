from flask import Flask, jsonify
import pymysql
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/atualizar_pacientes', methods=['POST', 'GET'])

def atualizar_pacientes():
    try:
        conex_origem = pymysql.connect(
            host=os.environ['HOST_MYSQL'],
            port=int(os.environ['PORT_MYSQL']),  
            user=os.environ['USER_MYSQL'],
            password=os.environ['PASS_MYSQL'],
            database=os.environ['DB_MYSQL']
)

        conex_dw = psycopg2.connect(
            host=os.environ['HOST_POSTGRES'],
            port=os.environ['PORT_POSTGRES'],  
            user=os.environ['USER_POSTGRES'],
            password=os.environ['PASS_POSTGRES'],
            database=os.environ['DB_POSTGRES']
)

        db_origem = conex_origem.cursor()
        db_destino = conex_dw.cursor()

        db_origem.execute("""
                            select idpaciente, nome, endereco, dtnasc, rg, cpf, sexo, raca, 
                                    mae, pai, bairro, cidade, cep, estado,
                                    telefone1, telefone2, telefone3 
                            from paciente p """)

        pacientes = db_origem.fetchall()

        for p in pacientes:
            db_destino.execute("""
                INSERT INTO dim_paciente (
                    id_paciente_origem, nome, endereco, dtnasc, rg, cpf, sexo, raca, 
                    mae, pai, bairro, cidade, cep, estado,
                    telefone1, telefone2, telefone3 
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_paciente_origem)
                DO UPDATE SET
                    nome = EXCLUDED.nome,
                    endereco = EXCLUDED.endereco,
                    dtnasc = EXCLUDED.dtnasc,
                    rg = EXCLUDED.rg,
                    cpf = EXCLUDED.cpf,
                    sexo = EXCLUDED.sexo,
                    raca = EXCLUDED.raca,
                    mae = EXCLUDED.mae,
                    pai = EXCLUDED.pai,
                    bairro = EXCLUDED.bairro,
                    cidade = EXCLUDED.cidade,
                    cep = EXCLUDED.cep,
                    estado = EXCLUDED.estado,
                    telefone1 = EXCLUDED.telefone1,
                    telefone2 = EXCLUDED.telefone2,
                    telefone3 = EXCLUDED.telefone3
            """, p)
            
        conex_dw.commit()
            
        db_origem.close()
        db_destino.close()
        conex_origem.close()
        conex_dw.close()
        
        return jsonify({"mensagem": "Dados atualizados com sucesso!"})
    
    except Exception as e:
        return jsonify({"erro": str(e)})
    
# agendador
sched = BackgroundScheduler(daemon=True)
sched.add_job(atualizar_pacientes, 'interval', hours=1)
sched.start()

@app.route('/atualizar_pacientes', methods=['POST', 'GET'])
def endpoint_atualizar():
    atualizar_pacientes()
    return jsonify({"mensagem": "Atualização iniciada manualmente!"})

if __name__ == '__main__':
    app.run(debug=True)
