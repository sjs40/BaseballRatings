class Fielder:

    def __init__(self, firstName, lastName, playerID, stint, teamID, pos, g, gs, innOuts, po, a, e, dp, pb, wp, sb, cs, zr):
        self.firstName = firstName
        self.lastName = lastName
        self.playerID = playerID
        self.stint = stint
        self.teamID = teamID
        self.pos = pos
        self.g = g
        self.gs = gs
        self.innOuts = innOuts
        self.po = po
        self.a = a
        self.e = e
        self.dp = dp
        self.pb = pb if pb is int else 0
        self.wp = wp if wp is int else 0
        self.sb = sb if sb is int else 0
        self.cs = cs if cs is int else 0
        self.zr = zr if zr is int else 0

    def combine_fielder(self, other):
        return Fielder(self.firstName, self.lastName, self.playerID, 1, other.teamID, self.pos, self.g + other.g,
                       self.gs + other.gs, self.innOuts + other.innOuts, self.po + other.po, self.a + other.a,
                       self.e + other.e, self.dp + other.dp, self.pb + other.pb, self.wp + other.wp,
                       self.sb + other.sb, self.cs + other.cs, self.zr + other.zr)

    def combine_fielder_pos(self, other):
        prime_pos = self.pos if self.g > other.g else other.pos
        return Fielder(self.firstName, self.lastName, self.playerID, self.stint, self.teamID, prime_pos,
                       self.g + other.g, self.gs + other.gs, self.innOuts + other.innOuts, self.po + other.po,
                       self.a + other.a, self.e + other.e, self.dp + other.dp, self.pb + other.pb,
                       self.wp + other.wp, self.sb + other.sb, self.cs + other.cs, self.zr + other.zr)