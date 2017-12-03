import socket
import sys
import ast

#NOTE: CETTE VERSION NE FONCTIONNE PAS SUR LE PROGRAMME PRINCIPAL
#POUR UNE RAISON INCONNUE LE PROGRAMME N'AIME PAS LES COMMENTAIRES
#APRES CES 4 LIGNES SUIVANTES:


HOST = '109.15.170.36'
PORT = 2007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

def login(name,paswd):
    #Fonction qui gére la connection elle prend en paramètre 2 string contenant le nom et le mot de pass
    #Elle retourne -1 en cas de mauvais login 0 en cas de succès
    s.sendall("LOGIN".encode('UTF-8'))
    s.recv(1024)
    s.sendall(name.encode('UTF-8'))
    s.recv(1024)
    s.sendall(paswd.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    d = s.recv(1024).decode('UTF-8')
    if d == 'Bad Loggin':
        return -1
    return 0


def signup(name,passwd):
    #Fonction qui gére la création de compte elle prend en paramètre 2 string contenant le nom et le mot de passe
    #Elle retourne -1 si le nom d'utilisateur est pris et 0 en cas de succès
    s.sendall("SIGNUP".encode('UTF-8'))
    s.recv(1024)
    s.sendall(name.encode('UTF-8'))
    s.recv(1024)
    s.sendall(passwd.encode('UTF-8'))
    d = s.recv(1024).decode('UTF-8')
    if d == 'Username':
        #Username already taken
        return -1
    return 0

def getia():
    #Fonction qui récupère l'ia de l'utilisateur et la renvoye sous forme de string
    s.sendall('GETIA'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    size = int(s.recv(1024).decode('UTF-8'))
    text = ""
    i=0
    s.sendall('OK'.encode('UTF-8'))
    while i<size:
        text = text + s.recv(4096).decode('UTF-8')
        i = i + 4096
    return text


def buy(item,typ,price):
    #Fonction qui réalise l'achat d'un objet. Elle prend 3 string en parametre : le numero de l'item, le type de l'item et son prix
    s.sendall('BUY'.encode('UTF-8'))
    s.recv(1024)
    s.sendall(item.encode('UTF-8'))
    s.recv(1024)
    s.sendall(typ.encode('UTF-8'))
    s.recv(1024)
    s.sendall(price.encode('UTF-8'))
    d = s.recv(1024).decode('UTF-8')
    if d == 'Already bought':
        return -1
    elif d == 'Not enough money':
        return -2
    else:
        return 0


def equipe(item,typ):
    #Fonction qui equipe un item. Elle prend en paramètre 2 string : le numero de l'item et son type
    s.sendall('EQUIPE'.encode('UTF-8'))
    s.recv(1024)
    s.sendall(item.encode('UTF-8'))
    s.recv(1024)
    s.sendall(typ.encode('UTF-8'))


def aggression():
    #Fonction qui change la valeur d'aggression de l'utilisateur
    s.sendall('AGGR'.encode('UTF-8'))
    s.recv(1024)


def game():
    #Fonction qui lance la partie et retourne le resultat sous forme de liste de liste
    s.sendall('PLAY'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    size = int(s.recv(1024).decode('UTF-8'))
    s.sendall('OK'.encode('UTF-8'))
    i = 0
    oldb = 0
    buff = ""
    print(size)
    while i<size:
        buff = buff + s.recv(size+1).decode('UTF-8')
        i = i + len(buff)-oldb
        oldb=len(buff)
        print(i)
    return ast.literal_eval(buff)


def inv():
    #Fonction qui récupère tout l'inventaire de l'utilisateur et le renvoye sous forme de 4 dictionnaire
    s.sendall('getinvw'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    n = int(s.recv(1024).decode('UTF-8'))
    s.sendall('OK'.encode('UTF-8'))
    j = 0
    w = []
    while j < n-1:
        w.append(ast.literal_eval((s.recv(4096).decode('UTF-8'))[11:-2]))
        j = j + 1
        s.sendall('OK'.encode('UTF-8'))
    w.append(ast.literal_eval((s.recv(4096).decode('UTF-8'))[11:-2]))


    s.sendall('getinva'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    n = int(s.recv(1024).decode('UTF-8'))
    s.sendall('OK'.encode('UTF-8'))
    j = 0
    a = []
    while j < n-1:
        a.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))
        j = j + 1
        s.sendall('OK'.encode('UTF-8'))
    a.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))


    s.sendall('getinvc'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    n = int(s.recv(1024).decode('UTF-8'))
    s.sendall('OK'.encode('UTF-8'))
    j = 0
    c = []
    while j < n-1:
        c.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))
        j = j + 1
        s.sendall('OK'.encode('UTF-8'))
    c.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))

    s.sendall('getinvn'.encode('UTF-8'))
    s.recv(1024)
    s.sendall('OK'.encode('UTF-8'))
    n = int(s.recv(1024).decode('UTF-8'))
    s.sendall('OK'.encode('UTF-8'))
    j = 0
    na = []
    while j < n-1:
        na.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))
        j = j + 1
        s.sendall('OK'.encode('UTF-8'))
    na.append(ast.literal_eval(s.recv(4096).decode('UTF-8')[11:-2]))

    return w,a,c,na


def fin():
    #Fonction qui met fin a la connection
    s.sendall('FIN'.encode('UTF-8'))
    s.close()


def save(text):
    #Fonction qui sauvegarde l'ia, elle prends en paramètre l'ia sous forme de string
    s.sendall('SAVE'.encode('UTF-8'))
    s.recv(1024)
    s.sendall(str(len(text)).encode('UTF-8'))
    s.recv(1024)
    s.sendall(text.encode('UTF-8'))

def money():
    #Fonction qui renvoye l'argent de l'utilisateur
    s.sendall('MONEY'.encode('UTF-8'))
    return int(s.recv(1024).decode('UTF-8'))


def tank():
    #Fonction qui renvoye une liste contenant le nom des objet equiper par l'utilisateur
    s.sendall('TANK'.encode('UTF-8'))
    a = ast.literal_eval(s.recv(4096).decode('UTF-8').replace('<','"').replace('>','"'))
    a[0]=a[0][7:].strip()
    a[1]=a[1][6:].strip()
    a[2]=a[2][12:].strip()
    a[3]=a[3][10:].strip()
    return a
