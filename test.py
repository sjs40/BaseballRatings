import pymysql
from Batter import Batter
from Fielder import Fielder
from League import League
from Team import Team
import config

db = pymysql.connect(host=config.host, port=config.port, user=config.user, database=config.database, password=config.password)
cur = db.cursor(pymysql.cursors.DictCursor)

sql = "SELECT Batting.*, MasterTable.nameFirst, MasterTable.nameLast FROM Batting, MasterTable WHERE yearID = 2016 AND MasterTable.playerID = Batting.playerID;"
"""
sql = "SELECT Batting.*, Fielding.*, MasterTable.nameFirst, MasterTable.nameLast " \
            "FROM Batting, Fielding, MasterTable " \
            "WHERE Batting.yearID = 2016 AND Fielding.yearID = 2016 " \
            "AND Batting.playerID = MasterTable.playerID " \
            "AND MasterTable.playerID = Fielding.playerID;"
"""

batters = []
cur.execute(sql)

for row in cur:
    batter = Batter(row['nameFirst'], row['nameLast'], row['playerID'],  row['stint'], row['teamID'], row['lgID'], row['G'],
                    row['AB'], row['R'], row['H'], row['2B'], row['3B'], row['HR'],
                    row['RBI'], row['SB'], row['CS'], row['BB'], row['SO'], row['IBB'],
                    row['HBP'], row['SH'], row['SF'], row['GIDP'])
    batters.append(batter)


league = League(batters)
league.condense_batters()

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