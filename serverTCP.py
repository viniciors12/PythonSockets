import socket
import Queue
import pickle
# Create a Socket ( connect two computers)
import threading

queue = Queue.Queue()
all_connections = []
all_address = []
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            if (len(all_connections)<=10):
                conn, address = s.accept()
                s.setblocking(True)  # prevents timeout
                all_connections.append(conn)
                all_address.append(address)
                t = threading.Thread(target=processor,args=(conn,address,))
                t.daemon = True
                t.start()
                print("Conection has been established! |" + " IP " + address[0] + "| Port" + str(address[1]))

        except:
            print("Error accepting connections")

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def downloading(conn,addr):
    recv = conn.recv(1024)
    file = recv.decode("utf-8")
    f = open("./downloaded/" + file, "rb")
    while True:
        content = f.read(1024)
        conn.send(content)
        print(content)
        if not content:
            conn.send(b'3nd?tr4ns')
            break
    print("El archivo ha sido enviado correctamente.")
    f.close()

def uploading(conn,addr):
    recv = conn.recv(1024)
    file = recv.decode("utf-8")
    print(file)
    f = open("./uploaded/"+ file, "wb")
    while True:
        try:
            input_data = conn.recv(1024)
        except:
            print("Error de lectura.")
            break
        else:
            if input_data:
                # Compatibilidad con Python 3.
                if isinstance(input_data, bytes):
                    end = input_data[0] == 1
                else:
                    end = input_data == chr(1)
                if not end:
                    # Almacenar datos.
                    f.write(input_data)
                else:
                    break

    print("El archivo se ha recibido correctamente.")
    f.close()

def processor(conn,adress):
    print("procesando...")
    while True:
        data = conn.recv(1024)
        decode = data.decode("utf-8").split(' ')
        if decode[0]=='-d':
            downloading(conn, adress)
        elif decode[0]=='-u':
            uploading(conn, adress)
        elif decode[0]=='-l':
            print("Listar archivo")
        else:
            print("Comando desconcido")

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        queue.task_done()

#create_workers()
#create_jobs()
