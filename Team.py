class Team:

    def __init__(self, lg_batters, teamID):
        self.batters = []
        for b in lg_batters:
            if b.teamID == teamID:
                self.batters.append(b)
