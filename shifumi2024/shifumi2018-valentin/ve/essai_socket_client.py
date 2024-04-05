# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

import socket, sys


HOST = '192.168.1.168'
HOST = '0.0.0.0'
PORT = 50000

# 1) création du socket :
print('création du socket')
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) envoi d'une requête de connexion au serveur :
print("envoi d'une requête de connexion au serveur")
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()

print("Connexion établie avec le serveur.")

# 3) Dialogue avec le serveur :
msgServeur = mySocket.recv(1024).decode("Utf8")
while 1:
    if msgServeur.upper() == "FIN" or msgServeur =="":
        break
    print("S>", msgServeur)
    msgClient = input("C> ")
    mySocket.send(msgClient.encode("Utf8"))
    msgServeur = mySocket.recv(1024).decode("Utf8")

# 4) Fermeture de la connexion :
print("Connexion interrompue.")
mySocket.close()
