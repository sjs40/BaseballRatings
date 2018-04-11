import pymysql
import numpy as np
import scipy.stats as st

class Bat:

    def __init__(self, team_id, database):
        self.teamID = team_id
        self.database = database
        sql = 'CALL get_team_bat_by_id(%s);'
        cur = database.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, team_id)
        for row in cur:
            self.num_of_batters = row['numOfBatters']
            self.bat_age = row['batAge']
            self.g = row['G']
            self.pa = row['PA']
            self.ab = row['AB']
            self.r = row['R']
            self.h = row['H']
            self.b2 = row['2B']
            self.b3 = row['3B']
            self.hr = row['HR']
            self.rbi = row['RBI']
            self.sb = row['SB']
            self.cs = row['CS']
            self.bb = row['BB']
            self.so = row['SO']
            self.gdp = row['GDP']
            self.hbp = row['HBP']
            self.sh = row['SH']
            self.sf = row['SF']
            self.ibb = row['IBB']
            self.lob = row['LOB']

        # derived
        self.runs_per_game = float(self.r) / float(self.g)
        self.ba = float(self.h) / float(self.ab)
        self.obp = float(self.h + self.bb + self.hbp) / float(self.ab + self.bb + self.hbp + self.sf)
        self.total_bases = self.h + self.b2 + (self.b3 * 2) + (self.hr * 3)
        self.slg = float(self.total_bases) / float(self.ab)
        self.ops = self.obp + self.slg

        # ratings
        self.power = 0.0
        self.contact = 0.0
        self.scoring = 0.0
        self.overall = 0.0

    def set_power_rating(self, league_hr, league_slg):
        std_hr = np.std(league_hr)
        std_slg = np.std(league_slg)

        mean_hr = np.mean(league_hr)
        mean_slg = np.mean(league_slg)

        z_hr = (float(self.hr) - float(mean_hr)) / float(std_hr)
        z_slg = (float(self.slg) - float(mean_slg)) / float(std_slg)

        pct_hr = float(st.norm.cdf(z_hr)) * 100.0
        pct_slg = float(st.norm.cdf(z_slg)) * 100.0

        subtotal = (float(pct_hr) * 0.75) + (float(pct_slg) * 0.25)
        self.power = (subtotal * 0.4) + 60

    def set_contact_rating(self, league_ba, league_obp, league_h):
        std_ba = np.std(league_ba)
        std_obp = np.std(league_obp)
        std_h = np.std(league_h)

        mean_ba = np.mean(league_ba)
        mean_obp = np.mean(league_obp)
        mean_h = np.mean(league_h)

        z_ba = (float(self.ba) - float(mean_ba)) / float(std_ba)
        z_obp = (float(self.obp) - float(mean_obp)) / float(std_obp)
        z_h = (float(self.h) - float(mean_h)) / float(std_h)

        pct_ba = float(st.norm.cdf(z_ba)) * 100.0
        pct_obp = float(st.norm.cdf(z_obp)) * 100.0
        pct_h = float(st.norm.cdf(z_h)) * 100.0

        subtotal = (float(pct_ba) * 0.75) + (float(pct_obp) * 0.15) + (float(pct_h) * 0.1)
        self.contact = (subtotal * 0.4) + 60

    def set_scoring_rating(self, league_hr, league_rbi, league_r):
        std_hr = np.std(league_hr)
        std_rbi = np.std(league_rbi)
        std_r = np.std(league_r)

        mean_hr = np.mean(league_hr)
        mean_rbi = np.mean(league_rbi)
        mean_r = np.mean(league_r)

        z_hr = (float(self.hr) - float(mean_hr)) / float(std_hr)
        z_rbi = (float(self.rbi) - float(mean_rbi)) / float(std_rbi)
        z_r = (float(self.r) - float(mean_r)) / float(std_r)

        pct_hr = float(st.norm.cdf(z_hr)) * 100.0
        pct_rbi = float(st.norm.cdf(z_rbi)) * 100.0
        pct_r = float(st.norm.cdf(z_r)) * 100.0

        subtotal = (float(pct_hr) * 0.35) + (float(pct_rbi) * 0.5) + (float(pct_r) * 0.15)
        self.scoring = (float(subtotal) * 0.4) + 60

    def set_overall_rating(self):
        self.overall = (float(self.power) * 0.3) + (float(self.contact) * 0.3) + (float(self.scoring) * 0.4)

    def set_b_ratings(self, league_hr, league_slg, league_ba, league_obp, league_h, league_rbi, league_r):
        self.set_power_rating(league_hr, league_slg)
        self.set_contact_rating(league_ba, league_obp, league_h)
        self.set_scoring_rating(league_hr, league_rbi, league_r)
        self.set_overall_rating()

    def get_ratings_str(self):
        return 'Power: ' + str(round(self.power, 2)) + '\nContact: ' + str(round(self.contact, 2)) \
               + '\nScoring: ' + str(round(self.scoring, 2)) + '\nOverall: ' + str(round(self.overall, 2))