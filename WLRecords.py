#Developed by Ethan Shaotran, 2019

# IMPORTS
from __future__ import division
import pandas as pd
CurrentL1 = pd.read_csv('PolicyData/Current_L1.csv')
CurrentL1.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

CurrentL2 = pd.read_csv('PolicyData/Current_L2.csv')
CurrentL2.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

CurrentL3 = pd.read_csv('PolicyData/Current_L3.csv')
CurrentL3.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Current_Logan = pd.read_csv('PolicyData/Current_Logan.csv')
Current_Logan.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Current_SQ = pd.read_csv('PolicyData/Current_SQ.csv')
Current_SQ.columns = ['Wins', 'Ballots','Name','Code','School', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Current_NQ = pd.read_csv('PolicyData/Current_NQ.csv')
Current_NQ.columns = ['Wins','Ballots','Name','Code','School', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Past_L1 = pd.read_csv('PolicyData/Past_L1.csv')
Past_L1.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Past_L2 = pd.read_csv('PolicyData/Past_L2.csv')
Past_L2.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Past_L3 = pd.read_csv('PolicyData/Past_L3.csv')
Past_L3.columns = ['Wins','Name','Code','School',' ', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Past_SQ = pd.read_csv('PolicyData/Past_SQ.csv')
Past_SQ.columns = ['Wins', 'Ballots','Name','Code','School', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']

Past_NQ = pd.read_csv('PolicyData/Past_NQ.csv')
Past_NQ.columns = ['Wins', 'Ballots','Name','Code','School', ' ', 'Standard Team Name', 'Num Rounds', 'Weighting']






# TEAM LIST AGGREGATIONS (ALL, NQ)

ListOfTourns = [CurrentL1,CurrentL2,CurrentL3,Current_Logan,Current_SQ,Current_NQ,Past_L1,Past_L2,Past_L3,Past_SQ,Past_NQ]
ListOfTeams = []
ListOfTeamsFull = []
for Tournament in ListOfTourns:
    for team in range(1,Tournament.shape[0]):
        StdTeamName = Tournament.iloc[team,6]
        FullTeamName = "(" + str(Tournament['School'].iloc[team]) + ") " + str(Tournament['Name'].iloc[team])
        if StdTeamName not in ListOfTeams:
            ListOfTeams.append(StdTeamName)
            ListOfTeamsFull.append(FullTeamName)

ListOfNQTeams = Current_NQ.iloc[:,6][1:]


# RECORD CALCULATIONS

ListOfSingleTourns = [CurrentL1,CurrentL2,CurrentL3,Current_Logan,Past_L1,Past_L2,Past_L3]
ListOfPanelTourns = [Current_SQ,Past_SQ] #Past_NQ Separate
ListOfPastNQTourns = [Past_NQ]

records = pd.DataFrame(columns = ["Team Code", "Team Name", "Win Rate", "Win Rate Adj", "P(Breaking)","Wins", "Losses", "Logged Rounds"])

for index, team in enumerate(ListOfTeams):
    wins = 0
    rounds = 0
    winsadj = 0
    roundsadj = 0
    
    for Tournament in ListOfSingleTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum, 0])
        tournrounds = int(Tournament.iloc[1,7])
        tournweight = float(Tournament.iloc[1,8])
        wins+=tournwins
        rounds+=tournrounds
        winsadj+=tournwins * tournweight
        roundsadj+=tournrounds * tournweight
            
    for Tournament in ListOfPanelTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum, 1])
        tournrounds = int(Tournament.iloc[1,7])
        tournweight = float(Tournament.iloc[1,8])
        wins+=tournwins
        rounds+=tournrounds
        winsadj+=tournwins * tournweight
        roundsadj+=tournrounds * tournweight
    
    for Tournament in ListOfPastNQTourns:
        try:
            rownum = Tournament.iloc[:,6].tolist().index(team)
        except:
            continue #Skip to next tournament
        tournwins = int(Tournament.iloc[rownum,1])
        tournrounds = int(Tournament.iloc[rownum,7])
        tournweight = float(Tournament.iloc[1,8])
        wins+=tournwins
        rounds+=tournrounds
        winsadj+=tournwins * tournweight
        roundsadj+=tournrounds * tournweight

    if rounds > 0:
        winRate = wins/rounds
        winRateAdj = winsadj/roundsadj
    else:
        winRate = winRateAdj = 0
    
    #print(str(team)+": "+str(wins)+", "+str(rounds)+", "+str(WLrecord))
    
    losses = rounds - wins
    teamfullname = ListOfTeamsFull[index]
    
    Pbreak = winRateAdj**4 + 4*(winRateAdj**3)*(1-winRateAdj)
    
    records.loc[index] = [team, teamfullname, winRate, winRateAdj, Pbreak, wins, losses, rounds]




#DOWNLOAD
records = records.sort(['Win Rate', 'Logged Rounds'], ascending=[False, False])
records.to_csv('CFLRankings.csv', index=False)



