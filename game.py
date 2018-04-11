from Bat import Bat
from Pitch import Pitch
from Team import Team
from League import League
from Utils import Utils
import pymysql

class Game:

  def __init__(self, date, day, home_team_id, vis_team_id, time, league, db):
    self.date = date
    self.day = day
    self.vis_team_id = vis_team_id
    self.home_team_id = home_team_id
    self.time = time
    self.league = league

    self.vis_bat = Bat(vis_team_id, db)
    self.vis_pitch = Pitch(vis_team_id, db)
    self.vis_team = Team(vis_team_id, db, self.vis_bat, self.vis_pitch, league)

    self.home_bat = Bat(home_team_id, db)
    self.home_pitch = Pitch(home_team_id, db)
    self.home_team = Team(home_team_id, db, self.home_bat, self.home_pitch, league)

    self.h_pow_v_vs_pow, self.h_cont_v_vs_cont, \
    self.h_scor_v_vs_scor, self.h_b_over_b_p_over, \
    self.h_vs_pow_v_pow, self.h_vs_cont_v_cont, \
    self.h_vs_scor_v_scor, self.h_p_over_v_b_over = Utils.compare_teams(self.home_team, self.vis_team)
    self.total = Utils.compare_teams(self.home_team, self.vis_team)
    self.favorite, self.moneyline = Utils.get_moneyline(self.home_team, self.vis_team)

  def get_game_str(self):
    date_line = self.day + ', ' + str(self.date) + '\n'
    teams = self.home_team_id + ' vs. ' + self.vis_team_id + '\nRatings Comparisons:\n'
    pow_vs_pow = self.home_team_id + ' Power vs ' + self.vis_team_id + ' Pitch vs Power: ' + str(self.h_pow_v_vs_pow) + '\n'
    cont_vs_cont = self.home_team_id + ' Contact vs ' + self.vis_team_id + ' Pitch vs Contact: ' + str(self.h_cont_v_vs_cont) + '\n'
    scor_vs_scor = self.home_team_id + ' Scoring vs ' + self.vis_team_id + ' Pitch vs Scoring: ' + str(self.h_scor_v_vs_scor) + '\n'
    b_over_p_over = self.home_team_id + ' Batting vs ' + self.vis_team_id + ' Pitching: ' + str(self.h_b_over_b_p_over) + '\n\n'

    vs_pow_pow = self.home_team_id + ' Pitch vs Power vs ' + self.vis_team_id + ' Power: ' + str(self.h_vs_pow_v_pow) + '\n'
    vs_cont_cont = self.home_team_id + ' Pitch vs Contact vs ' + self.vis_team_id + ' Contact: ' + str(self.h_vs_cont_v_cont) + '\n'
    vs_scor_scor = self.home_team_id + ' Pitch vs Scoring vs ' + self.vis_team_id + ' Scoring: ' + str(self.h_vs_scor_v_scor) + '\n'
    p_over_b_over = self.home_team_id + ' Pitching vs ' + self.vis_team_id + ' Batting: ' + str(self.h_p_over_v_b_over) + '\n\n'
    overall = self.home_team_id + ' vs ' + self.vis_team_id + ' Net Overall: ' + str(sum(self.total)) + '\n'
    moneyline_str = self.favorite + ' ' + str(self.moneyline) + '\n'
    return date_line + teams + pow_vs_pow + cont_vs_cont + scor_vs_scor + b_over_p_over + vs_pow_pow + vs_cont_cont + vs_scor_scor + p_over_b_over + overall + moneyline_str


  def get_game_odds(self):
    home = self.home_team_id + ' (' + str(self.moneyline) + ')' if self.favorite == self.home_team_id else self.home_team_id
    vis = self.vis_team_id + ' (' + str(self.moneyline) + ')' if self.favorite == self.vis_team_id else self.vis_team_id
    date_line = self.day + ', ' + str(self.date) + '  |  ' + home + ' vs. ' + vis
    return date_line

