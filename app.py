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
  print(f"Listado de usuarios con clientes abiertos")
  
  # Agregamos la nueva conexion.
  usuarios[request.sid] = data["user_id"]
  # Mostramos listado
  for u in usuarios.keys():
    print(f'{Fore.GREEN}{u} : {usuarios[u]}{Fore.RESET}')
  print(f"{Fore.BLUE}Cantidad de clientes: {len(usuarios)}{Fore.RESET}")
    

@socketio.on('update_users')
def handle_update_users(data):

    print(f'''{Fore.RED}·············Actualizar Usuarios···················\n)
    Cantidad: {len(data)}, chequear cuantos estan con clientes abiertos\n
    ································{Fore.RESET}''')
    for usuario in data:
      for u in usuarios.keys():
        if usuario['_id'] == usuarios[u]: 
          print(f"{Fore.BLUE} Enviando a {usuarios[u]} - {u} {Fore.RESET}")
          emit('update',usuario,to=u)

@socketio.on('disconnect')
def desconectar():
  print(f'{Fore.YELLOW} DESCONECTAR se disparo {Fore.RESET}\n{request.sid}')
  if request.sid in usuarios.keys():
    deleted = usuarios.pop(request.sid)
    print(f'{Fore.RED}Desconectado {request.sid} con id: {deleted}{Fore.RESET}')

# Iniciamos
if __name__ == '__main__':
    socketio.run(app)

