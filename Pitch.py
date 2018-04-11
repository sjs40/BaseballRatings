import pymysql
import numpy as np
import scipy.stats as st

class Pitch:

    def __init__(self, team_id, database):
        self.team_id = team_id
        self.database = database
        sql = 'CALL get_team_pitch_by_id(%s);'
        cur = database.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, team_id)
        for row in cur:
            self.num_of_pitchers = row['numOfPitchers']
            self.pitch_age = row['pitchAge']
            self.w = row['W']
            self.l = row['L']
            self.g = row['G']
            self.gs = row['GS']
            self.gf = row['GF']
            self.t_sho = row['tSho']
            self.c_sho = row['cSho']
            self.sv = row['SV']
            self.ip = row['IP']
            self.h = row['H']
            self.r = row['R']
            self.er = row['ER']
            self.hr = row['HR']
            self.bb = row['BB']
            self.ibb = row['IBB']
            self.so = row['SO']
            self.hbp = row['HBP']
            self.bk = row['BK']
            self.wp = row['WP']
            self.bf = row['BF']
            self.lob = row['LOB']

        # derived
        self.runs_against_per_game = float(self.r) / float(self.g)
        self.w_l_percent = float(self.w) / float(self.l)
        self.era = 9 * float(self.er) / float(self.ip)
        self.whip = float(self.bb + self.h) / float(self.ip)
        self.h9 = 9 * float(self.h) / float(self.ip)
        self.hr9 = 9 * float(self.hr) / float(self.ip)
        self.bb9 = 9 * float(self.bb) / float(self.ip)
        self.so9 = 9 * float(self.so) / float(self.ip)
        self.sobb = float(self.so) / float(self.bb)

        # ratings
        self.vs_power = 0
        self.vs_contact = 0
        self.scoring = 0
        self.overall = 0

    def set_vs_power_rating(self, league_hr, league_hr9):
        std_hr = np.std(league_hr)
        std_hr9 = np.std(league_hr9)

        mean_hr = np.mean(league_hr)
        mean_hr9 = np.mean(league_hr9)

        z_hr = (float(self.hr) - float(mean_hr)) / float(std_hr)
        z_hr9 = (float(self.hr9) - float(mean_hr9)) / float(std_hr9)

        pct_hr = float(1.0 - st.norm.cdf(z_hr)) * 100.0
        pct_hr9 = float(1.0 - st.norm.cdf(z_hr9)) * 100.0

        subtotal = (float(pct_hr) * 0.8) + (float(pct_hr9) * 0.2)
        self.vs_power = (subtotal * 0.4) + 60

    def set_vs_contact_rating(self, league_so, league_h, league_h9, league_whip):
        std_so = np.std(league_so)
        std_h = np.std(league_h)
        std_h9 = np.std(league_h9)
        std_whip = np.std(league_whip)

        mean_so = np.mean(league_so)
        mean_h = np.mean(league_h)
        mean_h9 = np.mean(league_h9)
        mean_whip = np.mean(league_whip)

        z_so = (float(self.so) - float(mean_so)) / float(std_so)
        z_h = (float(self.h) - float(mean_h)) / float(std_h)
        z_h9 = (float(self.h9) - float(mean_h9)) / float(std_h9)
        z_whip = (float(self.whip) - float(mean_whip)) / float(std_whip)

        pct_so = float(st.norm.cdf(z_so)) * 100.0
        pct_h = float(1.0 - st.norm.cdf(z_h)) * 100.0
        pct_h9 = float(1.0 - st.norm.cdf(z_h9)) * 100.0
        pct_whip = float(1.0 - st.norm.cdf(z_whip)) * 100.0

        subtotal = (float(pct_so) * 0.25) + (float(pct_h) * 0.15) + (float(pct_h9) * 0.1) + (float(pct_whip) * 0.5)
        self.vs_contact = (subtotal * 0.4) + 60

    def set_scoring_rating(self, league_era, league_whip, league_r):
        std_era = np.std(league_era)
        std_whip = np.std(league_whip)
        std_r = np.std(league_r)

        mean_era = np.mean(league_era)
        mean_whip = np.mean(league_whip)
        mean_r = np.mean(league_r)

        z_era = (float(self.era) - float(mean_era)) / float(std_era)
        z_whip = (float(self.whip) - float(mean_whip)) / float(std_whip)
        z_r = (float(self.r) - float(mean_r)) / float(std_r)

        pct_era = float(1.0 - st.norm.cdf(z_era)) * 100.0
        pct_whip = float(1.0 - st.norm.cdf(z_whip)) * 100.0
        pct_r = float(1.0 - st.norm.cdf(z_r)) * 100.0

        subtotal = (float(pct_era) * 0.65) + (float(pct_whip) * 0.25) + (float(pct_r) * 0.1)
        self.scoring = (subtotal * 0.4) + 60

    def set_overall_rating(self):
        self.overall = (float(self.vs_power) * 0.25) + (float(self.vs_contact) * 0.3) + (float(self.scoring) * 0.45)

    def set_p_ratings(self, league_hr, league_hr9, league_so, league_h, league_h9, league_whip, league_era, league_r):
        self.set_vs_power_rating(league_hr, league_hr9)
        self.set_vs_contact_rating(league_so, league_h, league_h9, league_whip)
        self.set_scoring_rating(league_era, league_whip, league_r)
        self.set_overall_rating()

    def get_ratings_str(self):
        return 'vs Power: ' + str(round(self.vs_power, 2)) + '\nvs Contact: ' + str(round(self.vs_contact, 2)) \
               + '\nvs Scoring: ' + str(round(self.scoring, 2)) + '\nOverall: ' + str(round(self.overall, 2))
