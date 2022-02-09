import itertools
import pandas as pd
from itertools import combinations
import json
import pickle
import timeit
import time

tableau = None
tableau_action = None

def read_from_db ():
    global tableau
    global tableau_action
    try:
        tableau = json.load('tableau.json')
        tableau_action = json.load('tableau_action.json')
    except IOError:
        print('Tableau inexistant')

def save_to_db ():
    pickle.dump(tableau, open('tableau.pkl', 'wb'))
    pickle.dump(tableau_action, open('tableau_actions.pkl', "wb"))


actions = pd.read_csv("listeaction_1000.csv")
actions["Dividende"] = actions["Dividende"].str.replace(",", ".").astype(float)
#actions["Bénéfice (après 2 ans)"] = actions["Bénéfice (après 2 ans)"].str.replace("%", "")
actions["Bénéfice (après 2 ans)"] = actions["Bénéfice (après 2 ans)"].str.replace(",", ".").astype(float)

actions["Coût par action (en euros)"] = actions["Coût par action (en euros)"].str.replace(",", ".").astype(float)
actions = actions.drop(actions[actions['Coût par action (en euros)'] < 0.001].index, axis=0)


def glouton (actions: pd.DataFrame, budget=500 ): 
    Actions_choisi = ()
    actions = actions.sort_values ( by= "Dividende", ascending=False )
    #
    actions["Somme Cumulative"] = actions["Dividende"].cumsum()
    actions["Couts Cumulative"] = actions["Coût par action (en euros)"].cumsum()
    #print(actions[actions["Couts Cumulative"] < budget])
    actions = actions.sort_values ( by= "Bénéfice (après 2 ans)", ascending=False )
    actions["Somme Cumulative"] = actions["Dividende"].cumsum()
    actions["Couts Cumulative"] = actions["Coût par action (en euros)"].cumsum()

    Actions_choisi = (actions[actions["Couts Cumulative"] < budget])
    #print (actions[actions["Couts Cumulative"] < budget]["Couts Cumulative"].values[-1])
    budget_consome = actions[actions["Couts Cumulative"] < budget]["Couts Cumulative"].values[-1]
    actions = actions.drop(index=Actions_choisi.index)
    budget_restant = budget - budget_consome

    actions_trop_cher = (actions[actions["Coût par action (en euros)"] > budget_restant])
    actions = actions.drop(actions_trop_cher.index)
    

    

    if not actions.empty:
        if len(actions) > 10:
            Actions_choisi = Actions_choisi.append(glouton(actions, budget_restant))
        else:
            Actions_choisi = Actions_choisi.append(bruteforce(actions, budget_restant))

    Actions_choisi["Somme Cumulative"] = Actions_choisi["Dividende"].cumsum()
    Actions_choisi["Couts Cumulative"] = Actions_choisi["Coût par action (en euros)"].cumsum()
    #print(actions[actions["Couts Cumulative"] < budget])
    Actions_choisi = Actions_choisi.sort_values ( by= "Bénéfice (après 2 ans)", ascending=False )
    Actions_choisi["Somme Cumulative"] = Actions_choisi["Dividende"].cumsum()
    Actions_choisi["Couts Cumulative"] = Actions_choisi["Coût par action (en euros)"].cumsum()
   
                    
    print(Actions_choisi)
    return Actions_choisi 



def bruteforce (actions: pd.DataFrame, budget: float):

    best_rendement = -1
    best_combinaison = pd.DataFrame()

    for i in range (1, len(actions) + 1):
        for panier_actions in itertools.combinations(actions.index, i):
            panier = actions.loc[panier_actions, :]
            rendement = panier['Dividende'].sum()
            if panier['Coût par action (en euros)'].sum() <= budget  \
               and rendement > best_rendement :
                best_combinaison = panier
                best_rendement = rendement
    return best_combinaison

        
glouton_result = glouton(actions)
print(glouton_result [["Coût par action (en euros)", "Dividende" ]].sum())

couts =  list (actions["Coût par action (en euros)"]) 
valeur = list (actions["Dividende"])

tableau = [[0] * 500 * 100 for _ in range  (len(actions))]
tableau_action = [[tuple()] * 500 * 100 for _ in range  (len(actions))]

actions.index = range(len(actions))
print (len(actions))
print( actions)

def dynamique (actions: pd.DataFrame, budget: float):
    action_trier = []
    timings = []
    debut = time.time() 
    for i, action in actions.iterrows():
        print(i)
    

        for j in range(budget * 100):
            cout_action = action["Coût par action (en euros)"] * 100
            if i == 0:
                tableau[0][j] = 0 if cout_action > j else action['Dividende']
                tableau_action[0][j] = tuple() if cout_action > j else (i, )
              
            else:
                
                if cout_action > j:
                    tableau[i][j] = tableau[i - 1][j]
                    tableau_action[i][j] = tableau_action[i - 1][j]
                else:
                    if action['Dividende'] >= max(tableau[i - 1][j], action['Dividende'] + tableau[i - 1][j - int(cout_action)]):
                        tableau[i][j] = action['Dividende']
                        tableau_action[i][j] = tuple() if cout_action > j else (i, )
                     
                
                    elif tableau[i -  1][j] >= (action['Dividende'] + tableau[i - 1][j - int(cout_action)]):
                        tableau[i][j] = tableau[i - 1][j]
                        tableau_action[i][j] = tableau_action[i - 1][j]
                        
                    else:
                        tableau[i][j] = action['Dividende'] + tableau[i - 1][j - int(cout_action)]
                        tableau_action[i][j] = (*tableau_action[i-1][j-int(cout_action)], i)
                        
                                    
      
        timings.append(time.time()- debut)
    print(tableau[-1][-1])
    print(actions.loc[tableau_action[-1][-1], :])
    actions[['Coût par action (en euros)', 'Dividende']].sum()
    return timings,action_trier



with open ("data.csv", "w") as s :

    for i, t in enumerate(dynamique(actions, 500)): 
        print(i, t, sep=',', file= s)
        print(tableau[-1][-1])
        print(actions.loc[tableau_action[-1][-1], :])
        actions[['Coût par action (en euros)', 'Dividende']].sum()
       

    

"""for i in range(1, len(actions) + 1):
    print(i, ',', timeit.timeit(lambda : glouton(actions[:i], 500), number=1), sep='')
df = pd.DataFrame(glouton_result)
df.to_csv("data.csv")
print(tableau[-1][-1])
print(tableau_action[-1][-1])
save_to_db()

"""

"""class ObjetSac: 
    def __init__(self, couts, valeur, indice): 
        self.indice = indice         
        self.poids = couts 
        self.valeur = valeur
        self.rapport = valeur // couts 
  #Fonction pour la comparaison entre deux ObjetSac
  #On compare le rapport calculé pour les trier
    def __lt__(self, other): 
        return self.rapport < other.rapport 
  
def getValeurMax(poids, valeurs, capacite): 
        tableauTrie = [] 
        for i in range(len(poids)): 
            tableauTrie.append(ObjetSac(poids[i], valeurs[i], i)) 
  
        #Trier les éléments du sac par leur rapport
        tableauTrie.sort(reverse = True) 
  
        compteurValeur = 0
        for objet in tableauTrie: 
            poidsCourant = int(objet.poids) 
            valeurCourante = int(objet.valeur) 
            if capacite - poidsCourant >= 0: 
                #on ajoute l'objet dans le sac
                #On soustrait la capacité
                capacite -= poidsCourant 
                compteurValeur += valeurCourante
                #On ajoute la valeur dans le sac 
        return compteurValeur 


print (getValeurMax(couts, valeur , 500))

"""