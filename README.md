# API de Atualização de Pacientes 🏥🔄  
Esta API foi desenvolvida para sincronizar dados de pacientes entre um banco de dados MySQL (origem) e um PostgreSQL (data warehouse), atualizando as informações periodicamente ou sob demanda.  


## Funcionalidades✨  

Sincronização automática (a cada hora)

Atualização manual via chamada API

Tratamento de conflitos (atualiza registros existentes)

Configuração segura com variáveis de ambiente  


## Tecnologias Utilizadas🛠️    


<img src="https://img.icons8.com/color/48/000000/python.png" width="16"/> Python

<img src="https://img.icons8.com/ios/50/000000/flask.png" width="16"/> Flask (framework web)

🐬 PyMySQL (conector MySQL)

🐘 Psycopg2 (conector PostgreSQL)

⏲️ APScheduler (agendamento de tarefas)

🔑 python-dotenv (gerenciamento de variáveis de ambiente)  

## Como Usar⚡    

### Pré-requisitos  
Python 3.x

Bancos MySQL (origem) e PostgreSQL (destino) configurados

Instalação
Clone o repositório

Instale as dependências:

**bash**  
pip install -r requirements.txt  

Crie um arquivo .env com suas credenciais  

### Endpoints  
GET/POST /atualizar_pacientes: Dispara a sincronização manual  

## Deploy no Render☁️    

Crie um novo Web Service

Adicione as variáveis de ambiente

Defina o comando: python app.py



