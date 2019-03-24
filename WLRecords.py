# IMPORTS
from __future__ import division
from collections import OrderedDict 
import pandas as pd
CurrentL1 = pd.read_csv('Current_L1.csv')
CurrentL2 = pd.read_csv('Current_L2.csv')
CurrentL3 = pd.read_csv('Current_L3.csv')
Current_Logan = pd.read_csv('Current_Logan.csv')
Current_SQ = pd.read_csv('Current_SQ.csv')
Current_NQ = pd.read_csv('Current_NQ.csv')
Past_L1 = pd.read_csv('Past_L1.csv')
Past_L2 = pd.read_csv('Past_L2.csv')
Past_L3 = pd.read_csv('Past_L3.csv')
Past_SQ = pd.read_csv('Past_SQ.csv')
Past_NQ = pd.read_csv('Past_NQ.csv')


# TEAM LIST AGGREGATIONS (ALL, NQ)

ListOfTourns = [CurrentL1,CurrentL2,CurrentL3,Current_Logan,Current_SQ,Current_NQ,Past_L1,Past_L2,Past_L3,Past_SQ,Past_NQ]
ListOfTeams = []
for Tournament in ListOfTourns:
    for team in range(1,Tournament.shape[0]):
        StdTeamName = Tournament.iloc[team,6]
        if StdTeamName not in ListOfTeams:
            ListOfTeams.append(StdTeamName)
ListOfTeams.sort()

ListOfNQTeams = Current_NQ.iloc[:,6][1:]


# RECORD CALCULATIONS

ListOfSingleTourns = [CurrentL1,CurrentL2,CurrentL3,Current_Logan,Past_L1,Past_L2,Past_L3]
ListOfPanelTourns = [Current_SQ,Past_SQ] #Past_NQ Separate
ListOfPastNQTourns = [Past_NQ]

records = {}

for team in ListOfTeams:
    wins = 0
    rounds = 0
    
    for Tournament in ListOfSingleTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum, 0])
        tournrounds = int(Tournament.iloc[1,7])
        wins+=tournwins
        rounds+=tournrounds
        
    #print(str(wins)+","+str(rounds))
    
    for Tournament in ListOfPanelTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum, 1])
        tournrounds = int(Tournament.iloc[1,7])
        wins+=tournwins
        rounds+=tournrounds
    
    #print(str(wins)+","+str(rounds))

    for Tournament in ListOfPastNQTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum,1])
        tournrounds = int(Tournament.iloc[rownum,7])
        wins+=tournwins
        rounds+=tournrounds

    if rounds > 0:
        WLrecord = wins/rounds
    else:
        WLrecord = 0
    
    #print(str(team)+": "+str(wins)+", "+str(rounds)+", "+str(WLrecord))
            
    records.update({team:WLrecord})


#DOWNLOAD THE RESULTS
records = OrderedDict(sorted(records.items(), key=lambda x: x[1], reverse=True))
TeamWLs = pd.DataFrame([records], columns=records.keys()).T
TeamWLs.to_csv('WLRecords.csv')



