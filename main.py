import serverTCP as tcp
import serverUDP as udp

def menu():

    print("-udp para utilizar UDP y -tcp para usar TCP ")
    while True:
        channel = raw_input('->')

        if channel == '-tcp':
            tcp.create_workers()
            tcp.create_jobs()
        elif channel == '-udp':
            udp.create_workers()
            udp.create_jobs()
        elif channel == 'salir':
            break
        else:
            print("Comando desconocido")


menu()