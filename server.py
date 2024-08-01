import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f'Servidor conectado en {host}:{port}')

clientes = []
usernames = []

def transmision(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)

def manejar_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if mensaje:
                print(f"Mensaje recibido: {mensaje.decode('utf-8')}")
                transmision(mensaje, cliente)
            else:
                break
        except:
            index = clientes.index(cliente)
            username = usernames[index]
            transmision(f'servidor: {username} desconectado'.encode('utf-8'), cliente)
            clientes.remove(cliente)
            usernames.remove(username)
            cliente.close()
            break

def recibir_conexiones():
    while True:
        cliente, direccion = server.accept()
        cliente.send('@username'.encode('utf-8'))
        username = cliente.recv(1024).decode('utf-8')
        clientes.append(cliente)
        usernames.append(username)
        print(f'Usuario conectado en {str(direccion)}')
        mensaje = f'Servidor: {username} se unio al chat'.encode('utf-8')

        transmision(mensaje, cliente)
        cliente.send('Conectado al servidor'.encode('utf-8'))

        thread = threading.Thread(target=manejar_mensajes, args=(cliente,))
        thread.start()

if __name__ == "__main__":
    recibir_conexiones()
