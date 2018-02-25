from scipy import stats
import math


class Batter:

    def __init__(self, firstName, lastName, playerID, stint, teamID, lgID, g, ab, r, h, b2, b3, hr, rbi, sb, cs, bb, so, ibb, hbp, sh, sf,
                 gidp):
        self.firstName = firstName
        self.lastName = lastName
        self.playerID = playerID
        self.position = "N/A"
        self.stint = float(stint)
        self.teamID = teamID
        self.lgID = lgID
        self.g = float(g)
        self.ab = float(ab)
        self.r = float(r)
        self.h = float(h)
        self.b2 = float(b2)
        self.b3 = float(b3)
        self.hr = float(hr)
        self.rbi = float(rbi)
        self.sb = float(sb)
        self.cs = float(cs)
        self.bb = float(bb)
        self.so = float(so)
        self.ibb = float(ibb)
        self.hbp = float(hbp)
        self.sh = float(sh)
        self.sf = float(sf)
        self.gidp = float(gidp)
        self.power_rate = 0
        self.slg = float((self.h + self.b2 + (self.b3 * 2) + (self.hr * 3)) / self.ab) if self.ab != 0 else 0.0
        self.pct_hr = 0
        self.speed_score = 0

    def set_position(self, pos):
        self.position = pos

    def get_string(self):
        return self.playerID + " " + str(self.stint) + " "

    def combine_batter(self, other):
        return Batter(self.firstName, self.lastName, self.playerID, 1, other.teamID, other.lgID, self.g + other.g,
                      self.ab + other.ab, self.r + other.r, self.h + other.h,
                      self.b2 + other.b2, self.b3 + other.b3, self.hr + other.hr,
                      self.rbi + other.rbi, self.sb + other.sb, self.cs + other.cs,
                      self.bb + other.bb, self.so + other.so, self.ibb + other.ibb,
                      self.hbp + other.hbp, self.sh + other.sh, self.sf + other.sf,
                      self.gidp + other.gidp)

    def get_power_rating(self, league):
        hr_per_h = self.hr / self.h if self.h != 0 else 0
        pct_hr_per_h = stats.percentileofscore(league.mlb_hr_per_h, hr_per_h)
        pct_ab = stats.percentileofscore(league.mlb_ab, self.ab)
        pct_slg = stats.percentileofscore(league.mlb_slg, self.slg)
        self.pct_hr = stats.percentileofscore(league.mlb_hr, self.hr)

        if pct_ab > 80:
            ab_multiplier = 1.0
        elif pct_ab > 60:
            ab_multiplier = .8
        elif pct_ab > 40:
            ab_multiplier = .6
        else:
            ab_multiplier = .4

        if self.pct_hr > 80:
            hr_multiplier = 1.0
        elif self.pct_hr > 60:
            hr_multiplier = 0.9
        elif self.pct_hr > 40:
            hr_multiplier = 0.75
        elif self.pct_hr > 20:
            hr_multiplier = 0.5
        else:
            hr_multiplier = 0.3
        self.power_rate = ((pct_hr_per_h * 0.85) + (pct_slg * 0.15)) * hr_multiplier

    def get_f1(self):
        term1 = ((1.0 * (self.sb + 3)) / (1.0 * (self.sb + self.cs + 7))) if (self.sb + self.cs + 7) != 0 else 0
        return 20 * (term1 - 0.4)

    def get_f2(self):
        term1 = 0.07
        b1 = self.h - self.b2 - self.b3 - self.hr
        term2 = (1.0 * (self.sb + self.cs)) / (1.0 * (b1 + self.bb + self.hbp)) if (b1 + self.bb + self.hbp) != 0 else 0
        return (math.sqrt(term2) * 1.0) / term1

    def get_f3(self):
        term1 = (1.0 * self.b3) / (self.ab - self.hr - self.so) if (self.ab - self.hr - self.so) != 0 else 0
        return (term1 * 1.0) / 0.0016

    def get_f4(self):
        term1 = (1.0 * (self.r - self.hr)) / (1.0 * (self.h + self.bb + self.hbp - self.hr)) if (self.h + self.bb + self.hbp - self.hr) != 0 else 0
        return 25 * (term1 - 0.1)

    def get_f5(self):
        term1 = (1.0 * self.gidp) / (1.0 * (self.ab - self.hr - self.so)) if (self.ab - self.hr - self.so) != 0 else 0
        return (0.063 - term1) / 0.007

    def set_speed_score(self):
        self.speed_score = (self.get_f1() + self.get_f2() + self.get_f3() + self.get_f4() + self.get_f5())
