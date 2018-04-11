from Utils import Utils

class Player:

  def __init__(self, row):
    self.playerID = row['playerID']
    self.teamID = row['teamID']
    self.g = row['g']
    self.ab = row['ab']
    self.r = row['r']
    self.h = row['h']
    self.b2 = row['2b']
    self.b3 = row['3b']
    self.hr = row['hr']
    self.rbi = row['rbi']
    self.sb = row['sb']
    self.cs = row['cs']
    self.bb = row['bb']
    self.so = row['so']
    self.ibb = row['ibb']
    self.hbp = row['hbp']
    self.sh = row['sh']
    self.sf = row['sf']
    self.gdp = row['gdp']
    self.birthCountry = row['country']
    self.birthYear = row['birthYear']
    self.birthMonth = row['birthMonth']
    self.birthDay = row['birthDay']
    self.nameFirst = row['nameFirst']
    self.nameLast = row['nameLast']
    self.weight = row['weight']
    self.height = row['height']
    self.bat = row['bat']
    self.throw = row['throw']

  def get_stats_str(self):
    return 'G: ' + str(self.g) + '\nAB: ' + str(self.ab) + '\nR: ' + str(self.r) + '\nH: ' + str(self.h) + '\n2B: ' \
           + str(self.b2) + '\n3B: ' + str(self.b3) + '\nHR: ' + str(self.hr) + '\nRBI: ' + str(self.rbi) + '\nSB: ' \
           + str(self.sb) + '\nCS: ' + str(self.cs) + '\nBB: ' + str(self.bb) + '\nSO: ' + str(self.so) + '\nIBB: ' \
           + str(self.ibb) + '\nHBP: ' + str(self.hbp) + '\nSH: ' + str(self.sh) + '\nSF: ' + str(self.sf) + '\nGDP: ' \
           + str(self.gdp) + '\n'

  def get_player_name_str(self):
    return self.nameFirst + ' ' + self.nameLast

  def get_player_info(self):
    return 'Height: ' + Utils.inches_to_feet(self.height) + ' Weight: ' + str(self.weight) + 'lbs\nBorn: ' + \
      str(self.birthMonth) + '/' + str(self.birthDay) + '/' + str(self.birthYear) + '\nCountry: ' + \
      self.birthCountry + '\nBats: ' + self.bat + ' Throws: ' + self.throw + '\n'