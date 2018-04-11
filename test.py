import pymysql
from Bat import Bat
from Pitch import Pitch
from Team import Team
from League import League
from Game import Game
from Player import Player
import config

db = pymysql.connect(host=config.host, port=config.port, user=config.user, database=config.database, password=config.password)
cur = db.cursor(pymysql.cursors.DictCursor)

sql = "CALL get_batter_by_name('Kris', 'Bryant');"

cur.execute(sql)

league = League(db)

'''
bats = []
pitches = []
for row in cur:
    id = row['teamID']
    bat = Bat(id, db)
    bat.set_power_rating(league.b_hr, league.b_slg)
    bat.set_contact_rating(league.b_ba, league.b_obp, league.b_h)
    bat.set_scoring_rating(league.b_hr, league.b_rbi, league.b_r)
    bat.set_overall_rating()
    bats.append(bat)
    print(id + " Power: " + str(int(round(bat.power, 0))) + " Contact: " + str(int(round(bat.contact, 0)))
          + " Scoring: " + str(int(round(bat.scoring, 0))) + " Overall: " + str(int(round(bat.overall, 0))))

    pitch = Pitch(id, db)
    pitch.set_vs_power_rating(league.p_hr, league.p_hr9)
    pitch.set_vs_contact_rating(league.p_so, league.p_h, league.p_h9, league.p_whip)
    pitch.set_scoring_rating(league.p_era, league.p_whip, league.p_r)
    pitch.set_overall_rating()
    pitches.append(pitch)
    print(id + " vs Power: " + str(int(round(pitch.vs_power, 0)))
          + " vs Contact: " + str(int(round(pitch.vs_contact, 0)))
          + " Scoring: " + str(int(round(pitch.scoring, 0)))
          + " Overall: " + str(int(round(pitch.overall, 0))))

games = []
for row in cur:
  date = str(row['date'])
  day = row['day']
  vis_team = row['vis']
  home_team = row['home']
  time = row['time']
  game = Game(date, day, home_team, vis_team, time, league, db)
  games.append(game)
  print(game.get_game_odds())
'''

for row in cur:
  player = Player(row)
  print(player.get_player_name_str())
  print(player.get_player_info())