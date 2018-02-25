class Team:

    # def __init__(self, lg_players, teamID):
    #     self.players = []
    #     for p in lg_players:
    #         if p.teamID == teamID:
    #             self.players.append(p)

    def __init__(self, teamID):
        self.players = []
        self.teamID = teamID

    def add_player(self, player):
        if player.teamID == self.teamID:
            self.players.append(player)
