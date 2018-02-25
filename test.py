import pymysql
from Batter import Batter
from Fielder import Fielder
from League import League
from Team import Team
import config

db = pymysql.connect(host=config.host, port=config.port, user=config.user, database=config.database, password=config.password)
cur = db.cursor(pymysql.cursors.DictCursor)

#sql = "SELECT Batting.*, MasterTable.nameFirst, MasterTable.nameLast FROM Batting, MasterTable WHERE yearID = 2016 AND MasterTable.playerID = Batting.playerID;"

sql = "SELECT Batting.*, Fielding.*, MasterTable.nameFirst, MasterTable.nameLast " \
            "FROM Batting, Fielding, MasterTable " \
            "WHERE Batting.yearID = 2016 AND Fielding.yearID = 2016 " \
            "AND Batting.playerID = MasterTable.playerID " \
            "AND MasterTable.playerID = Fielding.playerID;"


batters = []
fielders = []
prev_fielder = None
cur.execute(sql)

for row in cur:
    batter = Batter(row['nameFirst'], row['nameLast'],
                    row['playerID'],
                    row['stint'],
                    row['teamID'], row['lgID'], row['G'],
                    row['AB'], row['R'], row['H'], row['2B'], row['3B'], row['HR'],
                    row['RBI'], row['SB'], row['CS'], row['BB'], row['SO'], row['IBB'],
                    row['HBP'], row['SH'], row['SF'], row['GIDP'])
    batters.append(batter)

    fielder = Fielder(row['nameFirst'], row['nameLast'], row['Fielding.playerID'], row['Fielding.stint'],
                      row['Fielding.teamID'], row['POS'], row['Fielding.G'], row['GS'], row['InnOuts'],
                      row['PO'], row['A'], row['E'], row['DP'], row['PB'], row['WP'], row['Fielding.SB'],
                      row['Fielding.CS'], row['ZR'])

    if prev_fielder == None:
        fielders.append(fielder)
        prev_fielder = fielder
    elif prev_fielder.playerID != fielder.playerID or prev_fielder.pos != fielder.pos or prev_fielder.stint != fielder.stint:
        fielders.append(fielder)
        prev_fielder = fielder


league = League(batters, fielders)
league.condense_batters()
league.condense_fielders()
league.set_players()

'''
for b in league.batters:
    sql_position = "SELECT POS, G FROM Fielding WHERE yearID = 2016 AND playerID = \'" + b.playerID + "\';"
    prime_pos = "N/A"
    games = 0
    cursor = db.cursor()
    cursor.execute(sql_position)
    for row in cursor:
        if int(row[1]) > games:
            prime_pos = row[0]
    b.set_position(prime_pos)


league.calculate_avg_batter()
league.set_batter_ratings()

team = Team(league.batters, 'CHN')
for b in team.batters:
    print(
        b.firstName + " "
        + b.lastName + " "
        + b.position + " Speed: " + b.speed_label)
'''

team = league.teams['CHN']
for p in team.players:
    print(p.firstName + " " + p.lastName + " " + p.position + " Speed score: " + str(p.speed_score))