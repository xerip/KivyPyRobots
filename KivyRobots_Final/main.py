#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.9.0')


#importation des fichiers .py supplémentaires.

import clients
import database
import re

#Importations de toutes fonctions necessaires a notre  programme.
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty,StringProperty
from kivy.vector import Vector
from textwrap import dedent
from kivy.uix.textinput import TextInput

#Important pour faire fonctionner le programme.
#!!NE PAS OUBLIER LES DEUX LIGNES A LA FIN DU FICHIER!!
from kivy.lang import Builder

#On importe ici tout nos .kv
Builder.load_file("main.kv")
Builder.load_file("inventaire.kv")
Builder.load_file("Acceuil.kv")
Builder.load_file("boutique.kv")
Builder.load_file("tank.kv")
Builder.load_file("PageDeCode.kv")


#Nous avons difficilement pu faire communiquer les variables au travers du programme.
#Ainsi nous avons du hélas mettre tout dans le main.py

#Chaque groupe de définition relatif a une page est  séparé par des:

#########################################################################################################################


class GlobalApp(App):
    #On définit ici toutes les variables globales qui seront accédées au fil du programme avec GlobalApp.

    #valeurs pour connecter l'utilisateur.
    identifiant=StringProperty("Non Connecté")
    motdepasse=StringProperty("MotDePasse")
    argent=StringProperty("Argent : ")

    #Chemin du script de combat. Supposée modifiable.
    pathscript='combat.txt'
    logcombat=None

    #Variables utilisée pour l'aplication de combat:
    x=0
    event=None
    status=0
    #Les autres variables sont utilisées pour la boutique/inventaire.

    # nom de l'équipement séléctionné
    nomEq=StringProperty("Canon #1")
    # valeur de l'équipement séléctionné
    valEq=StringProperty("Attaque :    20")
    # prix de l'équipement séléctionné
    prixEq=StringProperty("Prix:    20")
    # image de l'équipement selectionné
    imgEq=StringProperty("img/cannon.png")
    # Equipement possédé par l'utilisateur
    equipement = ()
    # Equipement équipé actuellement par l'utilisateur:
    attaque = StringProperty("Attaque : ")
    defense = StringProperty("Defense : ")
    mouvement = StringProperty("Vitesse : ")
    ptaction = StringProperty("Pt d'Actions : ")
    # Leurs imageassociées
    attaquesource = StringProperty("img/cannon1.png")
    defensesource = StringProperty("img/armor1.png")
    mouvementsource = StringProperty("img/chenilles1.png")
    systemesource = StringProperty("img/system1.png")


    #mini fonction appelée au lancement pour faire apparaitre la fenetre de connection.
    def show_popup(self, dt):
        popupconnexion=FenetreConn()
        popupconnexion.open()

    #fenetre de lancement. Inclue une fonction au lancement et une fonction continue
    #qui verifie l'équipement de l'utilisateur pour l'affichage de l'inventaire/boutique (a optimiser)
    def build(self):
        Clock.schedule_once(self.show_popup, 1)
        game = Main()
        Clock.schedule_interval(game.test, 1)
        return game

#########################################################################################################################
#########################################################################################################################




class Main(Widget):
    #definitions des deux fonctions des boutons aide et connexion.



    def PopAide(self):
            Popup(title="Aide",content=Label(text='Bienvenue sur KivyRobot! \n Pour faire fonctionner ce jeu : \
            \n 1-CONNECTEZ VOUS (en haut a droite)\n Compte par défaut:a a\n La partie codage ne marche pas :(\
            \n 2- Mettez le script que vous voulez dans "combat.txt" dans votre dossier.  \
            \n 3- Vous pouvez acheter et equiper des equipements différents dans la boutique \
            \n 4-Appuyez sur combat ! Chaque combat donne 10$! \n \
            \n Note: Un cannon différent augmente portée et dégat, mais requiert plus de points d\'actions. \
            \n Ainsi si vous equipez le canon 3 avec le systeme de base, vous ne pourrez pas tirer.'),size_hint=(1,0.7)).open()


    def PopConnexion(self):
            popupconnexion=FenetreConn()
            popupconnexion.open()

    def test(self, dt):

        #Procédure pour que l'utilisateur voit ce qu'il a dans
        #son inventaire et acheté dans la boutique


        Rouage = ["Rouage1","Rouage2","Rouage3"]
        Process = ["Process1","Process2","Process3"]
        Blindage = ["Blindage1","Blindage2","Blindage3"]
        Canon = ["Canon1","Canon2","Canon3"]

        inventaire = self.ids['inventaire']
        boutique = self.ids['boutique']

        ChangingEquipementLayout = inventaire.ids['ChangingEquipementLayout']
        ChangingEquipementAcheteLayout = boutique.ids['ChangingEquipementLayout']

        # Rouages
        RouageLayout = ChangingEquipementLayout.ids["RouageLayout"]
        RouageAcheteLayout = ChangingEquipementAcheteLayout.ids["RouageLayout"]
        for i in Rouage:
            RouageLayout.ids[i].disabled = True
            RouageAcheteLayout.ids[i].disabled = False
        # Process
        ProcessLayout = ChangingEquipementLayout.ids["ProcessLayout"]
        ProcessAcheteLayout = ChangingEquipementAcheteLayout.ids["ProcessLayout"]
        for i in Process:
            ProcessLayout.ids[i].disabled = True
            ProcessAcheteLayout.ids[i].disabled = False

        # Blindage
        BlindageLayout = ChangingEquipementLayout.ids["BlindageLayout"]
        BlindageAcheteLayout = ChangingEquipementAcheteLayout.ids["BlindageLayout"]
        for i in Blindage:
            BlindageLayout.ids[i].disabled = True
            BlindageAcheteLayout.ids[i].disabled = False

        # Canon
        CanonLayout = ChangingEquipementLayout.ids["CanonLayout"]
        CanonAcheteLayout = ChangingEquipementAcheteLayout.ids["CanonLayout"]
        for i in Canon:
            CanonLayout.ids[i].disabled = True
            CanonAcheteLayout.ids[i].disabled = False

        # acces a  l'équipement par variable globale
        eq = GlobalApp.get_running_app().equipement

        # parcours du type d'objet
        for typeEq in eq:
            # parcours des objet
            for Eq in eq:
                for i in Eq:
                    # identifiant de l'équipement
                    idEq = i['name'].replace(" #","")
                    # identifiant du type de l'équipement (canon, blindage, etc.)
                    idType = i['name'][0:-3] + "Layout"
                    # equipement equipé
                    equipementLayout = ChangingEquipementLayout.ids[idType]
                    equipementButton = equipementLayout.ids[idEq]
                    equipementButton.disabled = False
                    # equipement acheter
                    equipementAcheteLayout = ChangingEquipementAcheteLayout.ids[idType]
                    equipementAcheteButton = equipementAcheteLayout.ids[idEq]
                    equipementAcheteButton.disabled = True



#Définitions des fonctionnalités du PopUp de connexion.
class FenetreConn(Popup):
    #Fonction qui collecte et met a jour l'acceuil une fois la connexion effectuée.
    def signing(root,x,y):
            #La fonction get_running_app() sert a recuperer/modifier une valeur globale.
            #Elle est utilisée au travers du programme pour cela.
            GlobalApp.get_running_app().identifiant = "User : " + x
            GlobalApp.get_running_app().equipement = clients.inv()
            GlobalApp.get_running_app().argent = "Argent : " + str(clients.money())
            GlobalApp.get_running_app().nomEq="Canon #1"
            GlobalApp.get_running_app().valEq="Attaque :    20"
            GlobalApp.get_running_app().prixEq="Prix:    20"
            GlobalApp.get_running_app().imgEq="img/cannon.png"
            FenetreConn.equipementmaj(root)

    #fonction qui récupère les valeurs précise de l'équipement a afficher dans la database.
    def equipementmaj(root):
        g=clients.tank()
        i=0
        while i<4:
            h=g[i]
            inve=database.recup(i,h[-1])
            if i==0:
                GlobalApp.get_running_app().attaque = "Attaque : " + str(inve[0])
                GlobalApp.get_running_app().attaquesource=str(inve[3])
            if i==1:
                GlobalApp.get_running_app().defense = "Defense : " + str(inve[0])
                GlobalApp.get_running_app().defensesource=str(inve[3])
            if i==2:
                GlobalApp.get_running_app().mouvement = "Vitesse : " + str(inve[0])
                GlobalApp.get_running_app().mouvementsource=str(inve[3])
            if i==3:
                GlobalApp.get_running_app().ptaction = "Pt d'Actions : " + str(inve[0])
                GlobalApp.get_running_app().systemesource=str(inve[3])

            i=i+1

    #Fonction de connexion au serveur. Avec message d'erreur sinon
    def changeident(root,x,y):
        retour=clients.login(x,y)
        if (retour==-1):
            Popup(title="Erreur",content=Label(text='Erreur:Compte/Mdp incorrect.\n Veuillez recommencer.'),size_hint=(0.6,0.3)).open()
        else:
            FenetreConn.signing(root,x,y)
            root.dismiss()

    #fonction de création d'un compte. Le serveur se connecte automatiquement si un compte est crée.
    def signup(root,x,y):
        retour=clients.signup(x,y)
        if (retour==-1):
            Popup(title="Erreur",content=Label(text='Erreur:Compte deja créé!\n Veuillez recommencer.'),size_hint=(0.6,0.3)).open()
        if (retour==0):
            FenetreConn.signing(root,x,y)
            Popup(title="Bravo!",content=Label(text='Compte créé!\n Vous etes également deja connecté!\n'),size_hint=(0.6,0.3)).open()
            root.dismiss()

    #S'assure que l'on soit connecté pour fermer la fenêtre de connexion.
    #Le programme n'est pas adapté a une nivagation sans connexion.
    def close(root):
        if GlobalApp.get_running_app().identifiant=="Non Connecté":
            popupalert=Popup(title="Erreur!",content=Label(text='Veuillez vous connecter!'),size_hint=(0.4,0.2)).open()
        else:
            root.dismiss()

#Fenetre appellée par le pop up de connexion.
class FenetreClose(Popup):
    pass


#########################################################################################################################





#définitions des fonctions de la page d'acceuil, CAD: Le bouton combat.Charger ne marche pas.
class Acceuil(Widget):
    def CallCombat(self):
        if GlobalApp.get_running_app().identifiant=="No Script":
            popupaide=Popup(title="Erreur!",content=Label(text='Veuillez charger un script!'),size_hint=(0.4,0.2)).open()
        else:
            with open(GlobalApp.get_running_app().pathscript, 'r') as fichiercombat:
                scriptcombat = fichiercombat.read()
                clients.save(scriptcombat)
        GlobalApp.get_running_app().logcombat=clients.game()
        game=TankGame()
        popuptank=FenetreCombat(title="Combat!",content=game).open()
        GlobalApp.get_running_app().event = Clock.schedule_interval(game.update,0.2)
        resultat=(GlobalApp.get_running_app().logcombat[-1][0])

        while (GlobalApp.get_running_app().status == 1):
            Clock.schedule_interval(1)
        GlobalApp.get_running_app().argent = "Argent : " + str(clients.money())

    def Charger(self):
        self._popup = ChargerScript()
        self._popup.open()

#définition nécéssaire pour l'appel.
class FenetreCombat(Popup):
    pass

#fonction incomplete qui devait récuperer l'addresse d'un script choisit.
class ChargerScript(Popup):
    def load(self,y):
        GlobalApp.get_running_app().pathscript=str(y)
        #y = re.split('\\W+',y)
        print (y)
        self.dismiss()
    pass










#########################################################################################################################









#On définit ici les fonctions utilisée pour afficher l'inventaire.
class Inventaire(Widget):

    def ButtonPress(self, id):

        #Fait fonctionner les boutons de séléction correctement.
        #Soulignement en mode partagé pour chaque boutton,
        #Changement du choix d'équipement en fonction du boutons,
        # -> Si "Cannon" choisit, liste des cannons affiché.

        #Liste des Buttons et des Widgets correspondant

        listButtonId = {
            'CanonButton' : ('CanonButton', 'CanonLayout'),
            'BlindageButton' : ('BlindageButton', 'BlindageLayout'),
            'ChenilleButton' : ('ChenilleButton', 'RouageLayout'),
            'SystemesButton' : ('SystemesButton', 'ProcessLayout'),
        }

        # Il faut indiquer l'id du widget qui contient les widget
        # On modifie de maniere indirect un widget
        ChangingEquipementLayout = self.ids["ChangingEquipementLayout"]


        # Recherche du boutton appelant.
        for i in listButtonId:
            if i == id:

                #Modification des widgets concerné.

                idButton = listButtonId[i][0]
                idLayout = listButtonId[i][1]
                # Modification des bouttons.
                selectButton = self.ids[idButton]
                selectButton.background_normal = 'img/selctEq.png'

                # Modification des layout.
                selectLayout = ChangingEquipementLayout.ids[idLayout]
                selectLayout.size_hint = (1,1)

            else:
                idButton = listButtonId[i][0]
                idLayout = listButtonId[i][1]
                # Modification des bouttons.
                selectButton = self.ids[idButton]
                selectButton.background_normal = ''

                # Modification des layout.
                selectLayout = ChangingEquipementLayout.ids[idLayout]
                selectLayout.size_hint = (0.01,0.01)

    def infoEq(self,nom,val,prix):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix

    def Equiper(self):
        # type 1 = canon, 2 = armure, 3 = chenille, 4 = Process
        type = GlobalApp.get_running_app().nomEq
        type = re.split('\W+',type)
        # num de l'item
        id = type[1]
        if type[0] == 'Canon':
            type = "1"
        elif type[0] == 'Chenille':
            type = "3"
        elif type[0] == 'Armure':
            type = "2"
        elif type[0] == 'Systeme':
            type = "4"
        clients.equipe(id,type)
        self.equipementmajour()


    #Fonction qui met a jour l'acceuil une fois un nouvel equipement équipé.
    def equipementmajour(self):
        g=clients.tank()
        i=0
        while i<4:
            h=g[i]
            inve=database.recup(i,h[-1])
            if i==0:
                GlobalApp.get_running_app().attaque = "Attaque : " + str(inve[0])
                GlobalApp.get_running_app().attaquesource=str(inve[3])
            if i==1:
                GlobalApp.get_running_app().defense = "Defense : " + str(inve[0])
                GlobalApp.get_running_app().defensesource=str(inve[3])
            if i==2:
                GlobalApp.get_running_app().mouvement = "Vitesse : " + str(inve[0])
                GlobalApp.get_running_app().mouvementsource=str(inve[3])
            if i==3:
                GlobalApp.get_running_app().ptaction = "Pt d'Actions : " + str(inve[0])
                GlobalApp.get_running_app().systemesource=str(inve[3])
            i=i+1

#Définition de chaque sous layout de l'interface.

class SelectCanonLayout(Widget):

    def infoEq(self,nom,val,prix,img):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix
        GlobalApp.get_running_app().imgEq = "img/cannon"+str(img)+".png"


class SelectArmorLayout(Widget):

    def infoEq(self,nom,val,prix,img):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix
        GlobalApp.get_running_app().imgEq = "img/armor"+str(img)+".png"


class SelectTrackLayout(Widget):

    def infoEq(self,nom,val,prix,img):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix
        GlobalApp.get_running_app().imgEq = "img/chenilles"+str(img)+".png"


class SelectSystemLayout(Widget):

    def infoEq(self,nom,val,prix,img):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix
        GlobalApp.get_running_app().imgEq = "img/system"+str(img)+".png"



#########################################################################################################################






#Définition de l'interface de la boutique: Celle ci est quasi similaire a l'inventaire.

class Boutique(Widget):
    def ButtonPress(self, id):
        #Fait fonctionner les boutons de séléction correctement.

        #Soulignement en mode partagé pour chaque boutton,
        #Changement du choix d'équipement en fonction du boutons,
        # -> Si "Cannon" choisit, liste des cannons affiché.

        #Liste des Buttons et des Widgets correspondant

        listButtonId = {
            'CanonButton' : ('CanonButton', 'CanonLayout'),
            'BlindageButton' : ('BlindageButton', 'BlindageLayout'),
            'ChenilleButton' : ('ChenilleButton', 'RouageLayout'),
            'SystemesButton' : ('SystemesButton', 'ProcessLayout'),
        }

        # Il faut indiquer l'id du widget qui contient les widget
        # On modifie de maniere indirect un widget
        ChangingEquipementLayout = self.ids["ChangingEquipementLayout"]


        # Recherche du boutton appelant.
        for i in listButtonId:
            if i == id:

                #Modification des widgets concerné.


                idButton = listButtonId[i][0]
                idLayout = listButtonId[i][1]
                # Modification des bouttons.
                selectButton = self.ids[idButton]
                selectButton.background_normal = 'img/selctEq.png'

                # Modification des layout.
                selectLayout = ChangingEquipementLayout.ids[idLayout]
                selectLayout.size_hint = (1,1)

            else:
                idButton = listButtonId[i][0]
                idLayout = listButtonId[i][1]
                # Modification des bouttons.
                selectButton = self.ids[idButton]
                selectButton.background_normal = ''

                # Modification des layout.
                selectLayout = ChangingEquipementLayout.ids[idLayout]
                selectLayout.size_hint = (0.01,0.01)

    def infoEq(self,nom,val,prix):
        GlobalApp.get_running_app().nomEq = nom
        GlobalApp.get_running_app().valEq = val
        GlobalApp.get_running_app().prixEq = prix

    def Acheter(self):
        # type 1 = canon, 2 = armure, 3 = chenille, 4 = Process
        type = GlobalApp.get_running_app().nomEq
        type = re.split('\W+',type)
        # num de l'item
        id = type[1]
        if type[0] == 'Canon':
            type = "1"
        elif type[0] == 'Chenille':
            type = "3"
        elif type[0] == 'Armure':
            type = "2"
        elif type[0] == 'Systeme':
            type = "4"
        # prix de l'équipement
        prix = GlobalApp.get_running_app().prixEq
        prix = prix[9:]


        clients.buy(id,type,prix)
        GlobalApp.get_running_app().equipement = clients.inv()
        GlobalApp.get_running_app().argent = "Argent : " + str(clients.money())





#########################################################################################################################



#Widget d'execution du combat: Ouvre et execute l'animation de combat.

class TankGame(Widget):
	#Classe principale de la simulation de combat
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    exp = ObjectProperty(None)


    def update(self,dt):
    	#Methode appeler pour passer a l'etape suivante du combat
        #logcombat contient toutes les actions effectuée par les deux scripts.
        res= GlobalApp.get_running_app().logcombat
        #x/i est le "lecteur" il parcourt  le script et effectue l'actione en conséquence
        i = GlobalApp.get_running_app().x
        self.exp.source = 'img/empty.png'			#On efface l'explosion précédente
        if(i==len(res)):
        	#On a fini d'executer le jeu sans que personne ne soit mort
            return
        if res[i][1] == 'dead':
        	#L'un des joueurs est mort, on arrete la boucle du jeu et on remet le lecteur a 0
            GlobalApp.get_running_app().event.cancel()
            if (res[i][0]==1):
                pop=Popup(title="Bravo!",size_hint=(.4,.2),content=Label(text="Vous Avez Gagné!")).open()
                GlobalApp.get_running_app().x=0
                return
            if (res[i][0]==0):
                pop=Popup(title="Oh non!",size_hint=(.4,.2),content=Label(text="Vous Avez Perdu!")).open()
                GlobalApp.get_running_app().x=0
                return
        if res[i][0] == 0:
        	#C'est une action pour le joueur 1
            if res[i][1] == 'moveRight':
                self.player1.moveright()
                self.player1.source = 'img/tankr.png'
            if res[i][1] == 'moveLeft':
                self.player1.moveleft()
                self.player1.source = 'img/tankl.png'
            if res[i][1] == 'moveUp':
                self.player1.moveup()
                self.player1.source = 'img/tankd.png'
            if res[i][1] == 'moveDown':
               self.player1.movedown()
               self.player1.source = 'img/tanku.png'
            if res[i][1] == 'shoot':
                self.exp.expl(res[i][2],res[i][3])
        if res[i][0] == 1:
        	#c'est une action pour le joueur 2
            if res[i][1] == 'moveRight':
                self.player2.moveright()
                self.player2.source = 'img/tankr2.png'
            if res[i][1] == 'moveLeft':
                self.player2.moveleft()
                self.player2.source = 'img/tankl2.png'
            if res[i][1] == 'moveUp':
                self.player2.moveup()
                self.player2.source = 'img/tankd2.png'
            if res[i][1] == 'moveDown':
                self.player2.movedown()
                self.player2.source = 'img/tanku2.png'
            if res[i][1] == 'shoot':
                self.exp.expl(res[i][2],res[i][3])

            #canvas.dismiss()
        #On incrémente la variable indiquant a quel etape nous en sommes
        GlobalApp.get_running_app().x = GlobalApp.get_running_app().x+1


class Explosion(Widget):
	#Widget qui gère les explosion du au tir.
    source = StringProperty('img/empty.png')
    def expl(self,x,y):
    	#Methode qui crée une explosion au coordonée x y
        self.x = self.width * x
        self.y = self.height * 34.8 -(self.height * (1+y))
        self.source = 'img/explosion.png'


class Tank(Widget):
	#Widget qui gère les tanks
    source = StringProperty('img/tanku2.png')
    x = NumericProperty()
    y = NumericProperty()
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def moveup(self):
    	#Deplace le tank vers le haut
        self.velocity_y -=self.height
        self.pos = Vector(*self.velocity) + self.pos
        self.velocity_y = 0

    def movedown(self):
    	#Deplace le tank vers le bas
        self.velocity_y +=self.height
        self.pos = Vector(*self.velocity) + self.pos
        self.velocity_y = 0

    def moveleft(self):
    	#Deplace le tank vers la gauche
        self.velocity_x -=self.width
        self.pos = Vector(*self.velocity) + self.pos
        self.velocity_x = 0

    def moveright(self):
    	#Deplace le tank vers la droite
        self.velocity_x +=self.width
        self.pos = Vector(*self.velocity) + self.pos
        self.velocity_x = 0




#########################################################################################################################


#classe lie a la fenetre de texte (incomplet!Ne marche pas!)
class MyTextInput(Widget):
    #s'active lorsqu'on est dans la zone de texte
    def write(self, instance, value):

        #liste fixe des mots possibles a autocomplete dans le programme
        word_list = ('and assert\
                break\
                char class close continue\
                def del\
                elif else exec except\
                for from false finally\
                global getTank\
                if is int input import include\
                len lambda\
                not\
                or open\
                pass print\
                read raise range return\
                str shoot\
                self.getTankId self.getEnemyTankId\
                self.getCellPosX self.getCellPosY\
                self.getCellDistance self.getCellFromXY\
                self.getPosition self.getLife self.getPM\
                self.getPA self.getRange self.moveTank self.shoot\
                try true\
                while write\
                yield').split(' ')

        letters='' #suite de lettre a garder en memoire

        match=False #True si il y a matching

        mot_complet=False #True si le mot est complet

        # initialsation de variables de type entier
        long_value=0
        long_suggestion=0

        #on met a jour la liste de mot a autocomplete qui est attribut de la classe
        word_list = list(set(
           word_list + value[:value.rfind(' ')].split(' ')))

        #on prend la suite de caractere ou est positionne sans les espaces
        val = (value[value.rfind(' ') + 1:])

        # pour modifier le text input
        moi = self.ids['code']

        #si val ne donne pas de valeur
        #ou si val est juste un espace par exemple
        if not val:
            moi.suggestion_text = ' '
            return

        try:
            #caractere ou on est positionne dans la zonr de texte
            newval=val[len(val)-1:]

            #si on se trouve dans le cas ou il peut y avoir autosuggestion
            if match==True:
                #on ajoute la suite de lettre memorise
                #au caractere ou on est positionne
                newval=letters+newval
                #on remet a jour la longueur du texte
                long_suggestion=len(val)
            #sinon
            else:
                #on remet a zero la suite de lettres
                letters=''
                #on remet a jour la longueur du texte
                long_suggestion=len(val)

            #si on ecrit le mot pouvant s'autocompleter en entier
            #sans utiliser l'autocompletion
            if mot_complet==True:
                mot_complet=False
                newval=val[len(val)-1:]
                #on remet a jour la longueur du texte
                long_suggestion=len(val)

            #si l'utilisateur vient d'utiliser l'autocompletion
            #c est a dire si la nouvelle longueur est plus petite
            #que l'ancienne longueur du texte + minimum 2 caractere (autocompletion faite)
            if long_value+2<=len(value):
                newval=val[len(val)-1:]
                #on remet a jour la longueur du texte
                long_suggestion=len(val)

            #si l'utilisateur vient d'utiliser un backspace
            #c'est a dire que la nouvelle longueur est plus
            #petite que l'ancienne longueur du texte
            if long_value>=len(value):
                newval=val[len(val)-1:]
                long_suggestion=len(val)



            #initialisation de liste qui contiendra les mots avec matching
            new_word_list=[]

            # on cree une liste de mots susceptible d'etre autocomplete
            # depuis la liste des mots de depart qui est fixe (word_list)
            # selon ce que l'utilisateur ecrit dans la zone de texte
            for w in word_list:
                if w.startswith(newval): #si w commence par newval
                    new_word_list=new_word_list+[w] #on l'ajoute dans la liste

            #si l'utilisateur a ecrit le mot en entier sans autocompletion
            if newval==new_word_list[0]:
                mot_complet=True #le mot est complet
                moi.text = ' '
                return

            #si au moins un mot peut etre autocomplete
            if len(new_word_list)!=0:
                letters=newval #on enregistre la lettre du mot
                match=True #on est dans le cas d'un matching
            #sinon
            else:
                match=False #on n'est pas dans le cas d'un matching
                letters='' #on remet a zero la

                #valeur de l'autocompletion

            moi.suggestion_text = new_word_list[0][long_suggestion:]

            #on garde l'ancienne longueur du texte en memoire
            long_value=len(value)

        #en cas d'erreur d'index
        except IndexError:

            print('!!! Index Error !!!')

            #on met une suggestion ' '
            moi.suggestion_text = ' '

            #on sort de la fonction
            return


    def keyboard_on_key_down(self, window, keycode, text, modifiers):

        #si la suggestion est non vide et que l'utilisateur
        #entre la touche '$' alors on ajoute au texte
        #la valeur de l'auto-suggestion
        if self.suggestion_text and keycode[1]=='²':
            self.insert_text(self.suggestion_text)
            return True
        #permet de redefinir la classe App et reutiliser la class MyTextInput
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

#########################################################################################################################





#FONCTION IMPERATIVE AU LANCEMENT DE l'APPLICATION:
if __name__ == "__main__" :

    KivyrobotApp = GlobalApp() #Cette ligne est également nécéssaire.
    KivyrobotApp.run()
