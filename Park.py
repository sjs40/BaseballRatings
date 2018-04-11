import pymysql

class Park:

  def __init__(self, team_id, database):
    self.team_id = team_id
    self.database = database
    sql = "CALL get_park_by_team(%s);"
    cur = self.database.cursor(pymysql.cursors.DictCursor)
    cur.execute(sql, team_id)
    for row in cur:
      self.name = row['name']
      self.city = row['city']
      self.state = row['state']
      self.r = row['r']
      self.hr = row['hr']
      self.h = row['h']
      self.b2 = row['2b']
      self.b3 = row['3b']
      self.bb = row['bb']

  def get_park_str(self):
    return self.team_id + '\n' + self.name + '\n' + self.city + ', ' + self.state + '\n\nPark Factors:\nHome Run: ' \
           + str(self.hr) + '\nHit: ' + str(self.h) + '\nWalk: ' + str(self.bb) + '\nDoubles: ' + str(self.b2) \
           + '\nTriples: ' + str(self.b3) + '\nRuns: ' + str(self.r) + '\n'

