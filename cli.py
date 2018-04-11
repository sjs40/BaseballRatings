import click
import pymysql
import config

from League import League
from Team import Team
from Bat import Bat
from Pitch import Pitch
from Game import Game
from Player import Player
from Park import Park

db = pymysql.connect(host=config.host, port=config.port, user=config.user, database=config.database, password=config.password)
cur = db.cursor(pymysql.cursors.DictCursor)

sql = "CALL get_team_ids();"

cur.execute(sql)
teams = []
for row in cur:
  teams.append(row['teamID'])

league = League(db)

@click.group()
def cli():
  pass

@cli.command()
@click.argument('name', nargs=1)
@click.option('--rating/--stats', default=True)
def team(name, rating):
  found = False
  for team in teams:
    if team == name:
      found = True
  if not found:
    click.echo('Team name is not valid.')
    return ''

  bat = Bat(name, db)
  pitch = Pitch(name, db)
  team = Team(name, db, bat, pitch, league)
  if rating:
    click.echo(team.get_ratings_str())
  else:
    click.echo(team.get_stats_str())

@cli.command()
@click.option('--name', default='none')
def games(name):
  if name == 'none':
    sql = 'CALL get_all_games();'
  else:
    sql = "CALL get_games_by_team('%s');" % name

  cursor = db.cursor(pymysql.cursors.DictCursor)
  cursor.execute(sql)

  for row in cursor:
    game = Game(row['date'], row['day'], row['home'], row['vis'], row['time'], league, db)
    click.echo(game.get_game_odds())

@cli.command()
@click.option('--first_name', prompt="Enter first name. If none, type 'NONE'")
@click.option('--last_name', prompt="Enter last name. If none, type 'NONE'")
def player(first_name, last_name):
  if first_name == 'NONE' and last_name == 'NONE':
    click.echo('Please enter a first and/or last name.')
    return ''
  elif first_name == 'NONE':
    sql = "CALL get_batter_by_last_name('{}');".format(last_name)
  elif last_name == 'NONE':
    sql = "CALL get_batter_by_first_name('{}');".format(first_name)
  else:
    sql = "CALL get_batter_by_name('{}', '{}');".format(first_name, last_name)

  cursor = db.cursor(pymysql.cursors.DictCursor)
  cursor.execute(sql)

  for row in cursor:
    player = Player(row)
    click.echo('\n')
    click.secho(player.get_player_name_str(), bold=True)
    click.echo(player.get_player_info())
    click.echo(player.get_stats_str())

@cli.command()
@click.argument('team_name', nargs=1)
def park(team_name):
  found = False
  for team in teams:
    if team == team_name:
      found = True
  if not found:
    click.echo('Team name is not valid.')
    return ''

  park = Park(team_name, db)
  click.echo(park.get_park_str())

@cli.command()
@click.argument('first_name', nargs=1)
@click.argument('last_name', nargs=1)
def college(first_name, last_name):
  sql = "CALL get_college_by_player('%s', '%s');"





if __name__ == '__main__':
  cli()