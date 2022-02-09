import itertools
import pandas as pd
from itertools import combinations
import json
import pickle
import timeit

tableau = None
tableau_action = None


actions = pd.read_csv("dataset1.csv")
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
            Actions_choisi = Actions_choisi.append(glouton(actions, budget_restant))
       
    Actions_choisi["Somme Cumulative"] = Actions_choisi["Dividende"].cumsum()
    Actions_choisi["Couts Cumulative"] = Actions_choisi["Coût par action (en euros)"].cumsum()
    #print(actions[actions["Couts Cumulative"] < budget])
    Actions_choisi = Actions_choisi.sort_values ( by= "Bénéfice (après 2 ans)", ascending=False )
    Actions_choisi["Somme Cumulative"] = Actions_choisi["Dividende"].cumsum()
    Actions_choisi["Couts Cumulative"] = Actions_choisi["Coût par action (en euros)"].cumsum()
   
                    
    print(Actions_choisi)
    return Actions_choisi 

    

for i in range(1, len(actions) + 1):
    print(i, ',', timeit.timeit(lambda : glouton(actions[:i], 500), number=1), sep='')

"""
print(tableau[-1][-1])
print(tableau_action[-1][-1])"""


"""
    

    if not actions.empty:
        if len(actions) > 15:
            Actions_choisi = Actions_choisi.append(glouton(actions, budget_restant))

        else:
            Actions_choisi = Actions_choisi.append(bruteforce(actions, budget_restant))
                    
    print(Actions_choisi)
    return Actions_choisi 
"""