from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from colorama import Fore, init

init()

load_dotenv(find_dotenv())
app = Flask(__name__)

# Configuracion
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['DEBUG'] = True if environ.get('DEBUG') == 'True' else False
app.config['PORT'] = 80

# Socketio
DOMAIN = environ.get('DOMAIN')
socketio = SocketIO(app, cors_allowed_origins="*")

""" 
Guardaremos en un diccionario los usuarios con sus datos

{
  'socket_id': user_id
}
"""
usuarios = dict()

@app.route('/')
def saludo():
  print("Hola")
  return f"Servidor socket para profut corriendo en {DOMAIN}"


@socketio.on('login')
def guardar_id(data):
  print(f'''{Fore.GREEN}·····························\n
  {str(data)}\n
  {Fore.RESET}
  ''')
  # print(f'{Fore.GREEN}id socket: {data["socket_id"]}\nid usuario: {data["user_id"]}{Fore.RESET}')
  print(f"Listado de usuarios con clientes abiertos")
  
  # Agregamos la nueva conexion.
  usuarios[request.sid] = data["user_id"]
  # join_room('room')
  # Mostramos listado
  for u in usuarios.keys():
    print(f'{Fore.GREEN}{u} : {usuarios[u]}{Fore.RESET}')
  print(f"{Fore.BLUE}Cantidad de clientes: {len(usuarios)}{Fore.RESET}")
    

@socketio.on('message')
def handle_message(data):

    print(f'''{Fore.RED}·············received message: {data} ···················\n)
    TIPO {type(data[0])}\n{data[0]}
    ································{Fore.RESET}''')
    dato=f"Enviando desde back en flask para user {request.sid}"
    hacer = True
    print(f"""{Fore.CYAN} Usuarios: {len(usuarios)} \n
    usuarios socketid:
    {str(usuarios)}
    {Fore.RESET}
    """)

    for u in usuarios.keys():
      if hacer:
        print(f"{Fore.CYAN} Enviando a {usuarios[u]} - {u} {Fore.RESET}")
        emit('update',{'msg':'XXXXXXXXXX','id':u},to=u)
        emit('update',{'msg':'QQQQQQ','id':u},broadcast=True)
      hacer=not hacer

@socketio.on('disconnect')
def desconectar():
  print(f'{Fore.YELLOW} DESCONECTAR se disparo {Fore.RESET}\n{request.sid}')
  if request.sid in usuarios.keys():
    deleted = usuarios.pop(request.sid)
    print(f'{Fore.RED}Desconectado {request.sid} con id: {deleted}{Fore.RESET}')

# Iniciamos
if __name__ == '__main__':
    socketio.run(app)

