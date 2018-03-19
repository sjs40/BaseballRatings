class Player:

    def __init__(self, batter, fielder):
        self.firstName = batter.firstName
        self.lastName = batter.lastName
        self.position = fielder.pos
        self.teamID = batter.teamID
        self.batter = batter
        self.fielder = fielder

        self.speed_score = 0
        self.contact_rate = 0

    def set_speed_label(self):
        self.batter.set_speed_score()
        speed_score_top = self.batter.speed_score
        term1 = (1.0 * (self.fielder.po + self.fielder.a)) / (1.0 * self.fielder.g) if self.fielder.g != 0 else 0
        if self.position == 'C':
            speed_score_top += 1
        elif self.position == '1B':
            speed_score_top += 2
        elif self.position == '2B':
            speed_score_top += ((term1 / 4.8) * 6)
        elif self.position == '3B':
            speed_score_top += ((term1 / 2.65) * 4)
        elif self.position == 'SS':
            speed_score_top += ((term1 / 4.6) * 7)
        elif self.position == 'OF':
            speed_score_top += ((term1 / 2.0) * 6)

        self.speed_score = round(speed_score_top / 6, 2)