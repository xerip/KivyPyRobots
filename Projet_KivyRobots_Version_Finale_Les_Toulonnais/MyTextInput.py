
from kivy.uix.widget import Widget

from kivy.app import App


class CodeApp(App):
    def build(self):
        return acceuil()

#classe lie a la fenetre de texte
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

blApp = CodeApp()

