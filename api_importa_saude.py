from flask import Flask, jsonify
import pymysql
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/atualizar_pacientes', methods=['POST', 'GET'])

def atualizar_pacientes():
    try:
        conex_origem = pymysql.connect(
            host = 'saude-prod.cxnjnmddnhrn.sa-east-1.rds.amazonaws.com',
            port = 3306,
            database = 'saude_braganca_paulista',
            user = 'rouser',
            password = 'haU@T8mp'
        )

        conex_dw = psycopg2.connect(
            host = 'localhost',
            port = '5432',
            dbname = 'geo_dw',
            user = 'postgres',
            password = '123'
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
                            insert into dim_paciente (
                            id_paciente_origem, nome, endereco, dtnasc, rg, cpf, sexo, raca, 
                            mae, pai, bairro, cidade, cep, estado,
                            telefone1, telefone2, telefone3 
                            )
                            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """, p)
            
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
