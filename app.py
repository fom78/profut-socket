from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from flask_socketio import SocketIO, emit
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
  print('·····························'+str(data))
  # print(f'{Fore.GREEN}id socket: {data["socket_id"]}\nid usuario: {data["user_id"]}{Fore.RESET}')
  print(f"Listado de usuarios con clientes abiertos")
  # for u in usuarios.keys():
  #   # Chequeamos si id de usuario ya existe, o sea ya hay un cliente, cerramos esa conexion.
  #   if usuarios[u] == data["user_id"]:
  #     print(f'{Fore.RED}{u} : {usuarios[u]}{Fore.RESET}')
  #     usuarios.pop(u)
  #   else:
  #     print(f'{Fore.GREEN}{u} : {usuarios[u]}{Fore.RESET}')
  # Agregamos la nueva conexion.
  usuarios[request.sid] = data["user_id"]
  
  # Mostramos listado
  for u in usuarios.keys():
    print(f'{Fore.GREEN}{u} : {usuarios[u]}{Fore.RESET}')
  print(f"{Fore.BLUE}Cantidad de clientes: {len(usuarios)}{Fore.RESET}")
    

@socketio.on('message')
def handle_message(data):
    print(f'·············received message: {data} ···················')
    print(f'{request.sid}')
    print(f'·············received message: {data} ···················')
    dato=f"Enviando desde back en flask para user {request.sid}"
    hacer = True
    print(f"{Fore.CYAN} Usuarios: {len(usuarios)} {Fore.RESET}")

    for u in usuarios.keys():
      if hacer:
        print(f"{Fore.CYAN} Enviando a {usuarios[u]} {Fore.RESET}")
        print(u)
        emit('update',dato,room=u)
        emit('update','ZZZZZZZZZZZZZZZZZZZZZZZ',broadcast= True)
      hacer=not hacer

@socketio.on('update_user')
def update(data):
  print(f"####### Enviar dato a un usuario particular segun id #####")
  # socketio.emit('update',)

@socketio.on('disconnect')
def desconectar():
  print(Fore.YELLOW + 'DESCONECTAR se disparo' + Fore.RESET)
  print(request.sid)
  if request.sid in usuarios.keys():
    deleted = usuarios.pop(request.sid)
    print(f'{Fore.RED}Desconectado {request.sid} con id: {deleted}{Fore.RESET}')

# Iniciamos
if __name__ == '__main__':
    socketio.run(app)

