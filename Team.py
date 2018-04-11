import pymysql

class Team:

    def __init__(self, team_id, database, bat, pitch, league):
        self.team_id = team_id
        self.database = database
        sql = 'CALL get_team_by_id(%s);'
        cur = database.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql, team_id)
        for row in cur:
            self.rank = row['rank']
            self.league = row['league']
            self.w = row['w']
            self.l = row['l']
            self.r = row['r']
            self.ra = row['ra']
            self.sos = row['sos']
            self.srs = row['srs']
            self.pyth_w = row['pythW']
            self.pyth_l = row['pythL']
            self.inter_w = row['interW']
            self.inter_l = row['interL']
            self.home_w = row['homeW']
            self.home_l = row['homeL']
            self.road_w = row['roadW']
            self.road_l = row['roadL']
            self.ex_inn_w = row['exInnW']
            self.ex_inn_l = row['exInnL']
            self.one_run_w = row['1RunW']
            self.one_run_l = row['1RunL']
            self.v_rhp_w = row['vRHPW']
            self.v_rhp_l = row['vRHPL']
            self.v_lhp_w = row['vLHPW']
            self.v_lhp_l = row['vLHPL']
            self.geq_500_w = row['GEQ500W']
            self.geq_500_l = row['GEQ500L']
            self.l_500_w = row['L500W']
            self.l_500_l = row['L500L']
            self.attendance = row['attendance']
            self.bpf = row['bpf']
            self.ppf = row['ppf']
            self.payroll = row['payroll']
            self.challenges = row['challenges']
            self.successes = row['successes']
            self.managers = row['managers']

        # derived
        self.w_l_percent = float(self.w) / float(self.l)
        self.r_diff = self.r - self.ra
        self.luck = self.w - self.pyth_w

        self.bat = bat
        self.pitch = pitch
        self.league = league
        self.bat.set_b_ratings(league.b_hr, league.b_slg, league.b_ba, league.b_obp, league.b_h, league.b_rbi, league.b_r)
        self.pitch.set_p_ratings(league.p_hr, league.p_hr9, league.p_so, league.p_h, league.p_h9, league.p_whip, league.p_era, league.p_r)

        self.power = self.bat.power
        self.contact = self.bat.contact
        self.scoring = self.bat.scoring
        self.b_overall = self.bat.overall

        self.vs_power = self.pitch.vs_power
        self.vs_contact = self.pitch.vs_contact
        self.vs_scoring = self.pitch.scoring
        self.p_overall = self.pitch.overall

    def get_ratings_str(self):
        return self.team_id + '\n\nBatting:\n' + self.bat.get_ratings_str() \
               + '\n\nPitching:\n' + self.pitch.get_ratings_str()

    def get_stats_str(self):
        return self.team_id + ' (' + str(self.w) + ' - ' + str(self.l) + ') ' + '\nSOS: ' + str(self.sos) + '\nSRS: ' \
               + str(self.srs) + '\nR: ' + str(self.r) + ' RA: ' + str(self.ra) + '\nPyth W-L: (' + str(self.pyth_w) \
               + ' - ' + str(self.pyth_l) + ')\nInter-league W-L: (' + str(self.inter_w) + ' - ' + str(self.inter_l) \
               + ')\nHome W-L: (' + str(self.home_w) + ' - ' + str(self.home_l) + ')\nRoad W-L: (' + str(self.road_w) \
               + ' - ' + str(self.road_l) + ')\nExtra Inning W-L: (' + str(self.ex_inn_w) + ' - ' + str(self.ex_inn_l) \
               + ')\n1 Run W-L: (' + str(self.one_run_w) + ' - ' + str(self.one_run_l) + ')\nvRHP W-L: (' + str(self.v_rhp_w) \
               + ' - ' + str(self.v_rhp_l) + ')\nvLHP W-L: (' + str(self.v_lhp_w) + ' - ' + ')\n>.500 W-L: (' \
               + str(self.geq_500_w) + ' - ' + str(self.geq_500_l) + ')\n<.500 W-L: (' + str(self.l_500_w) + ' - ' \
               + str(self.l_500_l) + ')\nAttendance: ' + str(self.attendance) + '\nBPF: ' + str(self.bpf) + '\nPPF: ' \
               + str(self.ppf) + '\nPayroll: $' + str(self.payroll) + '\nChallenges: ' + str(self.challenges) \
               + '\nSuccesses: ' + str(self.successes) + '\nManagers: ' + str(self.managers) + '\n'




