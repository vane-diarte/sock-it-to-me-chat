import socket
import threading

username = input('Ingresa tu usuario: ')

host = '127.0.0.1'
port = 55555

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect((host, port))



def recibir_mensajes():
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if mensaje == '@username':
                socket_cliente.send(username.encode('utf-8'))
            else:
                print(f'Recibido: {mensaje}')
        except Exception as e:
            print(f'Error al recibir mensaje: {e}')
            socket_cliente.close()
            break

def enviar_mensajes():
    while True:
        mensaje = f'{username}: {input("Mensaje ")}'
        socket_cliente.send(mensaje.encode('utf-8'))

recibir_hilo = threading.Thread(target=recibir_mensajes)
recibir_hilo.start()

enviar_hilo = threading.Thread(target=enviar_mensajes)
enviar_hilo.start()



