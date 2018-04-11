import pymysql

class League:

    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)

        ### BAT ###
        self.b_hr = []
        self.b_h = []
        self.b_rbi = []
        self.b_r = []
        self.b_2b = []
        self.b_3b = []
        self.b_ab = []
        self.b_bb = []
        self.b_hbp = []
        self.b_sf = []

        # derived
        self.b_ba = []
        self.b_slg = []
        self.b_obp = []
        self.b_rpg = []
        self.b_ops = []


        ### PITCH ###
        self.p_hr = []
        self.p_ip = []
        self.p_so = []
        self.p_h = []
        self.p_bb = []
        self.p_r = []
        self.p_er = []
        self.p_w = []

        # derived
        self.p_hr9 = []
        self.p_h9 = []
        self.p_so9 = []
        self.p_whip = []
        self.p_sobb = []
        self.p_era = []


        ### TEAM ###
        self.t_srs = []
        self.t_w = []
        self.t_l = []
        self.t_r = []
        self.t_ra = []
        self.t_pyth_w = []
        self.t_pyth_l = []
        self.t_home_w = []
        self.t_home_l = []
        self.t_road_w = []
        self.t_road_l = []
        self.t_extra_w = []
        self.t_extra_l = []
        self.t_1run_w = []
        self.t_1run_l = []
        self.t_geq500_w = []
        self.t_geq500_l = []
        self.t_l500_w = []
        self.t_l500_l = []
        self.t_attend = []

        # derived
        self.t_rpg = []
        self.t_rdiff = []
        self.t_luck = []
        self.t_wper_home = []
        self.t_wper_road = []
        self.t_wper_1run = []
        self.t_wper_extra = []
        self.t_wper_geq500 = []
        self.t_wper_l500 = []

        self.load_all_bat()
        self.load_all_pitch()
        self.load_all_team()


    def load_all_bat(self):
        sql_bat_total = 'CALL get_all_bat();'
        self.cur.execute(sql_bat_total)
        for row in self.cur:
            self.b_hr.append(row['HR'])
            self.b_h.append(row['H'])
            self.b_rbi.append(row['RBI'])
            self.b_r.append(row['R'])
            self.b_2b.append(row['2B'])
            self.b_3b.append(row['3B'])
            self.b_bb.append(row['BB'])
            self.b_ab.append(row['AB'])
            self.b_hbp.append(row['HBP'])
            self.b_sf.append(row['SF'])

            ba = float(row['H']) / float(row['AB'])
            slg = (float(row['H']) + float(row['2B']) + (float(row['3B']) * 2.0) + (float(row['HR']) * 3.0)) / float(row['AB'])
            obp = float(row['H'] + row['BB'] + row['HBP']) / float(row['AB'] + row['BB'] + row['HBP'] + row['SF'])
            rpg = float(row['R']) / 162.0
            ops = float(slg) + float(obp)

            self.b_ba.append(ba)
            self.b_slg.append(slg)
            self.b_obp.append(obp)
            self.b_rpg.append(rpg)
            self.b_ops.append(ops)

    def load_all_pitch(self):
        sql_pitch_total = 'CALL get_all_pitch();'
        self.cur.execute(sql_pitch_total)
        for row in self.cur:
            self.p_hr.append(row['HR'])
            self.p_ip.append(row['IP'])
            self.p_so.append(row['SO'])
            self.p_h.append(row['H'])
            self.p_bb.append(row['BB'])
            self.p_r.append(row['R'])
            self.p_er.append(row['ER'])
            self.p_w.append(row['W'])

            hr9 = 9.0 * (float(row['HR']) / float(row['IP']))
            h9 = 9.0 * (float(row['H']) / float(row['IP']))
            so9 = 9.0 * (float(row['SO']) / float(row['IP']))
            whip = float(row['BB'] + row['H']) / float(row['IP'])
            sobb = float(row['SO']) / float(row['BB'])
            era = 9.0 * (float(row['ER']) / float(row['IP']))

            self.p_hr9.append(hr9)
            self.p_h9.append(h9)
            self.p_so9.append(so9)
            self.p_whip.append(whip)
            self.p_sobb.append(sobb)
            self.p_era.append(era)

    def load_all_team(self):
        sql_team_total = 'CALL get_all_team();'
        self.cur.execute(sql_team_total)
        for row in self.cur:
            self.t_srs.append(row['srs'])
            self.t_w.append(row['w'])
            self.t_l.append(row['l'])
            self.t_r.append(row['r'])
            self.t_ra.append(row['ra'])
            self.t_pyth_w.append(row['pythW'])
            self.t_pyth_l.append(row['pythL'])
            self.t_home_w.append(row['homeW'])
            self.t_home_l.append(row['homeL'])
            self.t_road_w.append(row['roadW'])
            self.t_road_l.append(row['roadL'])
            self.t_extra_w.append(row['exInnW'])
            self.t_extra_l.append(row['exInnL'])
            self.t_1run_w.append(row['1RunW'])
            self.t_1run_l.append(row['1RunL'])
            self.t_geq500_w.append(row['GEQ500W'])
            self.t_geq500_l.append(row['GEQ500L'])
            self.t_l500_w.append(row['L500W'])
            self.t_l500_l.append(row['L500L'])
            self.t_attend.append(row['attendance'])

            rpg = float(row['r']) / 162.0
            rdiff = float(row['r']) - float(row['ra'])
            luck = float(row['pythW']) - float(row['w'])
            wper_home = (float(row['homeW']) / float(row['homeW'] + row['homeL'])) * 100.0
            wper_road = (float(row['roadW']) / float(row['roadW'] + row['roadL'])) * 100.0
            wper_1run = (float(row['1RunW']) / float(row['1RunW'] + row['1RunL'])) * 100.0
            wper_extra = (float(row['exInnW']) / float(row['exInnW'] + row['exInnL'])) * 100.0
            wper_geq500 = (float(row['GEQ500W']) / float(row['GEQ500W'] + row['GEQ500L'])) * 100.0
            wper_l500 = (float(row['L500W']) / float(row['L500W'] + row['L500L'])) * 100.0

            self.t_rpg.append(rpg)
            self.t_rdiff.append(rdiff)
            self.t_luck.append(luck)
            self.t_wper_home.append(wper_home)
            self.t_wper_road.append(wper_road)
            self.t_wper_1run.append(wper_1run)
            self.t_wper_extra.append(wper_extra)
            self.t_wper_geq500.append(wper_geq500)
            self.t_wper_l500.append(wper_l500)

