val=20

def recup(num,i):
    text=""
    if num==0:
        text="img/cannon"+i+".png"
    if num==1:
        text="img/armor"+i+".png"
    if num==2:
        text="img/chenilles"+i+".png"
    if num==3:
        text="img/system"+i+".png"
    if int(i)==3:
        i=4
    valeur=int(i)*val
    return(valeur,valeur,valeur,text)
