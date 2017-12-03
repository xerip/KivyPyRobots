# coding: utf-8

import socket
import sys
import threading
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Weapon, Armor, Caterpillar, NavSystem, TypeItem, Inventory, DefaultIa
from .models import UserProfile, Tank, Ia

from .funct.funct import getItemByType,getBoolInventory



class Cconn(threading.Thread):
    #Classe qui contient la fonction principal du serveur et les methode correspondant au différente commande
    def __init__(self,conn):
        #Initialisation des Thread et des variable
        threading.Thread.__init__(self)
        self.conn = conn            #Socket de connections
        self.user = None            #Utilisateur courant

    def run(self):
        #methode principale de la classe
        while True:
            #Boucle principale de la classe
            data = self.conn.recv(1024).decode('UTF-8')
            data = data.upper().strip()
            #On recoit et docode la commande envoyer par le client et selon celle ci pn execute la methode correspondante
            if data == 'SAVE':
                self.save()
            elif data == 'PLAY':
                self.play()
            elif data == 'LOGIN':
                self.login()
            elif data == 'SIGNUP':
                self.signup()
            elif data == 'GETIA':
                self.getia()
            elif data == 'GETINVA':
                self.getinva()
            elif data == 'GETINVW':
                self.getinvw()
            elif data == 'GETINVN':
                self.getinvn()
            elif data == 'GETINVC':
                self.getinvc()
            elif data == 'BUY':
                self.buy()
            elif data == 'EQUIPE':
                self.equipe()
            elif data == 'AGGR':
                self.aggression()
            elif data == 'GETWEAPON':
                self.weapon()
            elif data == 'GETCAT':
                self.cat()
            elif data == 'GETNAVSYS':
                self.navsys()
            elif data == 'GETARMOR':
                self.armor()
            elif data == 'MONEY':
                self.money()
            elif data == 'TANK':
                self.tanks()
            elif data == 'FIN':
                #Fin de la connection
                break
            else:
                reply = 'NA'
                self.conn.sendall(reply.encode('UTF-8'))
        self.conn.close()

    def login(self):
        #Methode qui s'occupe de la connection des utilisateur ayant déja un compte
        self.conn.sendall("Please Log in".encode('UTF-8'))
        username = self.conn.recv(1024).decode('UTF-8')
        self.conn.sendall('OK'.encode('UTF-8'))
        password = self.conn.recv(1024).decode('UTF-8')
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is None:
            #erreur d'authentification
            self.conn.sendall('Bad Loggin'.encode('UTF-8'))
        else:
            #l'utilisateur est connecté
            self.user = user
            self.conn.sendall('login success'.encode('UTF-8'))


    def save(self):
        #Methode qui sauvegarde l'ia envoyer par l'utilisateur comme etant la sienne
        self.conn.sendall('OK'.encode('UTF-8'))
        userprofile = UserProfile.objects.get(user=self.user)
        ai = Ia.objects.get(owner=userprofile)
        size = int(self.conn.recv(1024).decode('UTF-8'))
        self.conn.sendall('OK'.encode('UTF-8'))
        i=0
        text = ""
        while i<size:
            text = text + self.conn.recv(4096).decode('UTF-8')
            i = len(text)+1
        ai.text = text
        ai.save()


    def signup(self):
        #Methode s'occupant de la creation du compte d'un nouvelle utilisateur et de sa connection
        email = "N/A"
        self.conn.sendall('OK'.encode('UTF-8'))
        username = self.conn.recv(1024).decode('UTF-8')
        self.conn.sendall('OK'.encode('UTF-8'))
        password = self.conn.recv(1024).decode('UTF-8')
        try:
            #On test si le nom d'utilisateur est près
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = User.objects.create_user(username, email, password)
            #creation de l'utilisater
            UserProfile(user=user, money=0).save()
            #creation de l'ia
            userProfile = UserProfile.objects.get(user=user)
            i = Ia.objects.create(owner=userProfile, name=username+"\'s Ia", text=DefaultIa.objects.get(pk=1).text)
            #Inventaire par default
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=1))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=2))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=3))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=4))
            #Initialisation du tank
            w = getItemByType(1,TypeItem(pk=1))
            a = getItemByType(1,TypeItem(pk=2))
            c = getItemByType(1,TypeItem(pk=3))
            n = getItemByType(1,TypeItem(pk=4))
            Tank.objects.create(owner=userProfile, ia=i,weapon=w,armor=a,caterpillar=c,navSystem=n)
            self.user = user
            #Connection de l'utilisateur
            self.conn.sendall("Success".encode('UTF-8'))
            return 0
        self.conn.sendall("Username".encode('UTF-8'))

    def getia(self):
        #Methode qui récupère le code de l'ia
        self.conn.sendall('OK'.encode('UTF-8'))
        userProfile = UserProfile.objects.get(user = self.user)
        ia = Ia.objects.get(owner = userProfile)
        text = ia.text
        self.conn.recv(1024)
        self.conn.sendall(str(len(text)).encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(text.encode('UTF-8'))


    def getinvw(self):
        #Methode qui recupère les armes de l'utilisateur
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        inventory = UserProfile.objects.get(user=self.user).__getInventory__()
        weapon = inventory[0]
        l = []
        for i in weapon:
            l.append(Weapon.objects.filter(name = i.name))
        self.conn.sendall(str(len(l)).encode('UTF-8'))
        for i in l:
            self.conn.recv(1024)
            self.conn.sendall(str(i.values()).encode('UTF-8'))

    def getinva(self):
        #Methode qui recupère les blindages de l'utilisateur
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        inventory = UserProfile.objects.get(user=self.user).__getInventory__()
        armor = inventory[1]
        l = []
        for i in armor:
            l.append(Armor.objects.filter(name = i.name))
        self.conn.sendall(str(len(l)).encode('UTF-8'))
        for i in l:
            self.conn.recv(1024)
            self.conn.sendall(str(i.values()).encode('UTF-8'))

    def getinvc(self):
        #Methode qui recupère les chenilles de l'utilisateur
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        inventory = UserProfile.objects.get(user=self.user).__getInventory__()
        cat = inventory[2]
        l = []
        for i in cat:
            l.append(Caterpillar.objects.filter(name = i.name))
        self.conn.sendall(str(len(l)).encode('UTF-8'))
        for i in l:
            self.conn.recv(1024)
            self.conn.sendall(str(i.values()).encode('UTF-8'))

    def getinvn(self):
        #Methode qui récupère les systèmes de navigations de l'utilisateur
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        inventory = UserProfile.objects.get(user=self.user).__getInventory__()
        navsys = inventory[3]
        l = []
        for i in navsys:
            l.append(NavSystem.objects.filter(name = i.name))
        self.conn.sendall(str(len(l)).encode('UTF-8'))
        for i in l:
            self.conn.recv(1024)
            self.conn.sendall(str(i.values()).encode('UTF-8'))


    def buy(self):
        #Methode qui permet a l'utilisateur d'acheter des objet dans la boutique
        self.conn.sendall('OK'.encode('UTF-8'))
        user = UserProfile.objects.get(user=self.user)
        itemIn = int(self.conn.recv(1024).decode('UTF-8'))
        self.conn.sendall('OK'.encode('UTF-8'))
        typeIn = int(self.conn.recv(1024).decode('UTF-8'))
        self.conn.sendall('OK'.encode('UTF-8'))
        price = int(self.conn.recv(1024).decode('UTF-8'))

        boolTab = getBoolInventory(user)

        if boolTab[typeIn-1][itemIn-1]:
            conn.sendall('Already bought'.encode('UTF-8'))
            return 0
        elif price > user.money :
            self.conn.sendall('Not enough money'.encode('UTF-8'))
            return 0
        else :
            user.money = user.money - price
            user.save()
            Inventory.objects.create(owner=user,item=itemIn,typeItem=TypeItem(pk=typeIn))
            self.conn.sendall('OK'.encode('UTF-8'))


    def equipe(self):
        #Methode qui permet a l'utilisateur d'équiper des objets qu'il possède
        self.conn.sendall('OK'.encode('UTF-8'))
        userProfile = UserProfile.objects.get(user=self.user)
        tank = Tank.objects.get(owner=userProfile)
        itemIn = int(self.conn.recv(1024).decode('UTF-8'))
        self.conn.sendall('OK'.encode('UTF-8'))
        typeIn = self.conn.recv(1024).decode('UTF-8')
        if int(typeIn) == 1:
            w = getItemByType(itemIn, TypeItem(pk=1))
            tank.weapon = w
            tank.save()
        elif int(typeIn) == 2:
            a = getItemByType(itemIn, TypeItem(pk=2))
            tank.armor = a
            tank.save()
        elif int(typeIn) == 3:
            c = getItemByType(itemIn, TypeItem(pk=3))
            tank.caterpillar = c
            tank.save()
        elif int(typeIn) == 4:
            n = getItemByType(itemIn, TypeItem(pk=4))
            tank.navSystem = n
            tank.save()


    def aggression(self):
        #Methode qui change la valeur d'aggression de l'utilisateur
        self.conn.sendall('OK'.encode('UTF-8'))
        userProfile = UserProfile.objects.get(user=self.user)
        agressionValue = userProfile.agression
        userProfile.agression = not agressionValue
        userProfile.save()


    def play(self):
        #Methode qui lance la partie et renvoye le resultat de cette dernière
        self.conn.sendall('OK'.encode('UTF-8'))
        import random
        from .game.Game import Game
        user1 = UserProfile.objects.get(user=self.user)
        nbuser = UserProfile.objects.all().count()
        user2 = UserProfile.objects.get(user=self.user)
        while True :
            #tirage d'un addversaire aléatoirement
            alea = random.randrange(0, nbuser)
            try:
                user2 = UserProfile.objects.get(pk=alea)
            except UserProfile.DoesNotExist:
                pass
            if user1 != user2: break

        #On recupère les tank et ia des utilisateur
        tank1 = Tank.objects.get(owner=user1)
        tank2 = Tank.objects.get(owner=user2)
        ia1 = Ia.objects.get(owner=user1)
        ia2 = Ia.objects.get(owner=user2)
        #On initialise et lance le jeu
        game = Game(tank1, tank2, ia1, ia2)
        res = game.run(0)
        #On donne de l'argent au utilisateur
        user1.money = user1.money + 10
        user1.save()
        user2.money = user2.money + 10
        user2.save()
        #On encoye les resultats
        self.conn.recv(1024)
        self.conn.sendall(str(len(str(res))).encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(str(res).encode('UTF-8'))


    def weapon(self):
        #Methode qui récupère les armes existantes
        weapon = Weapon.objects.all()
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(str(weapon.values()).encode('UTF-8'))


    def armor(self):
        #Methode qui récupère les blindages
        armor = Armor.objects.all()
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(str(armor.values()).encode('UTF-8'))


    def cat(self):
        #Methode qui récupère les chenilles
        caterpillars = Caterpillar.objects.all()
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(str(caterpillars.values()).encode('UTF-8'))


    def navsys(self):
        #Methode qui récupère les systèmes de navigations
        navSys = NavSystem.objects.all()
        self.conn.sendall('OK'.encode('UTF-8'))
        self.conn.recv(1024)
        self.conn.sendall(str(navSys.values()).encode('UTF-8'))


    def money(self):
        #Methode qui recupère l'argent de l'utilisateur
        user = UserProfile.objects.get(user=self.user)
        self.conn.sendall(str(user.money).encode('UTF-8'))


    def tanks(self):
        #Methode qui récupère les objets equiper
        user = UserProfile.objects.get(user=self.user)
        tank = Tank.objects.get(owner=user)
        self.conn.sendall(str([tank.weapon,tank.armor,tank.caterpillar,tank.navSystem]).encode('UTF-8'))

def run():
    #Fonction qui lance le serveur
    HOST = '0.0.0.0'
    PORT = 2006
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket a l'addresse HOST sur le port PORT
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print("Bind failed. Error Code : " + str(msg.errno) + " Message " + msg.strerror)
        sys.exit()

    #On démare l'écoute
    s.listen(10)
    print("Serveur en écoute sur " + HOST + ":" + str(PORT))
    # La boucle d'attente des connexions
    while True:
        try:
            conn, addr = s.accept()
            print('Connection de ' + addr[0] + ':' + str(addr[1]))

            #On instancie la classe Cconn dès qu'un clients ce connecte
            t = Cconn(conn)
            t.start()

        except KeyboardInterrupt:
            print("Stop.\n")
            break
            s.close()
