
class Utils:

  @staticmethod
  def compare_teams(team_a, team_b):
    a_power_b_vs_power = int(round(team_a.power, 0)) - int(round(team_b.vs_power, 0))
    a_contact_b_vs_contact = int(round(team_a.contact, 0)) - int(round(team_b.vs_contact, 0))
    a_scoring_b_vs_scoring = int(round(team_a.scoring, 0)) - int(round(team_b.vs_scoring, 0))
    a_bat_overall_v_pitch_overall = int(round(team_a.b_overall, 0)) - int(round(team_b.p_overall, 0))

    a_vs_power_b_power = int(round(team_a.vs_power, 0)) - int(round(team_b.power, 0))
    a_vs_contact_b_contact = int(round(team_a.vs_contact, 0)) - int(round(team_b.contact, 0))
    a_vs_scoring_b_scoring = int(round(team_a.vs_scoring, 0)) - int(round(team_b.scoring, 0))
    a_p_overall_b_b_overall = int(round(team_a.p_overall, 0)) - int(round(team_b.b_overall, 0))

    return a_power_b_vs_power, a_contact_b_vs_contact, a_scoring_b_vs_scoring, a_bat_overall_v_pitch_overall,\
           a_vs_power_b_power, a_vs_contact_b_contact, a_vs_scoring_b_scoring, a_p_overall_b_b_overall

  @staticmethod
  def compare_teams_total(team_a, team_b):
    total = 0
    total += int(round(team_a.power, 0)) - int(round(team_b.vs_power, 0))
    total += int(round(team_a.contact, 0)) - int(round(team_b.vs_contact, 0))
    total += int(round(team_a.scoring, 0)) - int(round(team_b.vs_scoring, 0))
    total += int(round(team_a.b_overall, 0)) - int(round(team_b.p_overall, 0))
    total += int(round(team_a.vs_power, 0)) - int(round(team_b.power, 0))
    total += int(round(team_a.vs_contact, 0)) - int(round(team_b.contact, 0))
    total += int(round(team_a.vs_scoring, 0)) - int(round(team_b.scoring, 0))
    total += int(round(team_a.p_overall, 0)) - int(round(team_b.b_overall, 0))
    return total

  @staticmethod
  def get_moneyline(home, vis):
    total = Utils.compare_teams_total(home, vis)
    adj_total = total + 15 if total >= 0 else total - 15
    plus_100_total = ((adj_total + 100) * -1) if adj_total >= 0 else (adj_total - 100)
    favorite = home.team_id if adj_total >= 0 else vis.team_id
    return favorite, plus_100_total

  @staticmethod
  def inches_to_feet(inches):
    feet = int(inches / 12)
    extra_inches = inches % 12
    return str(feet) + "'" + str(extra_inches) + '"'
