import itertools
import csv
import timeit

# Ouvrir le fichier contenant la liste des actions et l'affecter a une variable ( actions )

with open ("listeaction_1000", "r") as l:
    l = csv.reader(l)

    actions = list(l)[1:]


# crée une fonction qui va contenir l'ago force brut
def f (actions):

    bestcombinaison = None
    
    # -1 pour etre sur qui n'y est pas de nombre négatif 
    bestrendement = -1 
    
    # faire une boucle qui va itérer sur la longueur de la liste
    for taille_panier in range (1,len(actions)+1): # de 1 au lieu de 0 +1 car si on commence a 0 on fini a 19 , ça permet d d'écaler l'index
        #print(F"{taille_panier}/20")
        # faire une boucle qui va générer toute les combinaisons [ itertools.combinations ] sur la liste d'actions [ actions ] jusqu'a la taille du panier [ len (actions)]
        for panier_action in itertools.combinations(actions,taille_panier):
            rendement = 0 
            cout = 0
            for action in panier_action: 
                rendement += float(action[-1].replace(",",".")) # rajoute rendement ou [0] au dernier élément [action] dans la liste [ panier d'action] et renplace "," par "." en presisant que c'est un float (ex : 1.0 )
                cout += float (action[1].replace(",", "."))
            if cout > 500: # continuer tant que le cout du panier n'exede pas 500
                continue

            if rendement > bestrendement: 
                bestcombinaison = panier_action 
                bestrendement = rendement

    print (bestcombinaison)
    print(bestrendement)


for i in range(1, len(actions) + 1):
    print(i, ',', timeit.timeit(lambda : f(actions[:i]), number=1), sep='')                                    
             
#print(timeit.timeit(f(actions), number=1)) # permet de s'avoir de le temps d'execution
#actions.extend(actions[:5])
#for i in range(1, len(actions) + 1):
    #print(i, ',', timeit.timeit(lambda : f(actions[:i]), number=2), sep='')