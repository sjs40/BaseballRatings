from Batter import Batter

class League:


    def __init__(self, batters):
        self.batters = batters
        self.avg_batter = None
        self.mlb_hr_per_h = []
        self.mlb_power_stats = []
        self.mlb_ab = []
        self.mlb_slg = []
        self.mlb_hr = []
        self.teamIDs = ['ARI', 'ATL', 'BAL', 'BOS', 'CHA', 'CHN', 'CIN', 'CLE', 'COL', 'DET',
                        'HOU', 'KCA', 'LAA', 'LAN', 'MIA', 'MIL', 'MIN', 'NYA', 'NYN', 'OAK',
                        'PHI', 'PIT', 'SDN', 'SEA', 'SFN', 'SLN', 'TBA', 'TEX', 'TOR', 'WAS']

    def condense_batters(self):
        new_batters = []
        temp_batter = None
        for b in self.batters:
            if temp_batter == None:
                temp_batter = b
            elif temp_batter.playerID != b.playerID:
                new_batters.append(temp_batter)
                temp_batter = b
            else:
                combined_b = temp_batter.combine_batter(b)
                temp_batter = combined_b
        new_batters.append(temp_batter)
        self.batters = new_batters

    def calculate_avg_batter(self):
        g = 0
        ab = 0
        r = 0
        h = 0
        b2 = 0
        b3 = 0
        hr = 0
        rbi = 0
        sb = 0
        cs = 0
        bb = 0
        so = 0
        ibb = 0
        hbp = 0
        sh = 0
        sf = 0
        gidp = 0

        for b in self.batters:
            g += b.g
            ab += b.ab
            r += b.r
            h += b.h
            b2 += b.b2
            b3 += b.b3
            hr += b.hr
            rbi += b.rbi
            sb += b.sb
            cs += b.cs
            bb += b.bb
            so += b.so
            ibb += b.ibb
            hbp += b.hbp
            sh += b.sh
            sf += b.sf
            gidp += b.gidp

        total_batters = len(self.batters)
        self.avg_batter = Batter("avg_batter", "avg_batter", "avg_batter", 1, "avg_batter", "avg_batter", float(g / total_batters),
                                 float(ab / total_batters), float(r / total_batters), float(h / total_batters),
                                 float(b2 / total_batters), float(b3 / total_batters), float(hr / total_batters),
                                 float(rbi / total_batters), float(sb / total_batters), float(cs / total_batters),
                                 float(bb / total_batters), float(so / total_batters), float(ibb / total_batters),
                                 float(hbp / total_batters), float(sh / total_batters), float(sf / total_batters),
                                 float(gidp / total_batters))

    def get_mlb_lists(self):
        self.mlb_hr_per_h = []
        self.mlb_power_stats = []
        self.mlb_ab = []
        self.mlb_hr = []
        self.mlb_slg = []
        for b in self.batters:
            hr_per_h = (b.hr / b.h) if b.h != 0 else 0
            self.mlb_hr_per_h.append(hr_per_h)
            self.mlb_power_stats.append((hr_per_h * .85) + (b.slg * .15))
            self.mlb_ab.append(b.ab)
            self.mlb_slg.append(b.slg)
            if b.hr > 0:
                self.mlb_hr.append(b.hr)

    def set_batter_ratings(self):
        self.get_mlb_lists()
        for b in self.batters:
            b.get_power_rating(self)
            b.get_speed_score()
