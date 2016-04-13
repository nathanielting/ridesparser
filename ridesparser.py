from datetime import *
from mailbox import *
from HTMLParser import HTMLParser

class Driver(object):
  """docstring for Driver"""
  def __init__(self, name):
    super(Driver, self).__init__()
    self.name = name
    self.rides = []
  def addRide(self,date):
    if date not in self.rides:
      self.rides.append(date)
  def __str__(self):
    return self.name
  def rideCount(self):
    return len(self.rides)

class DriverSet(object):
  """docstring for DriverSet"""
  def __init__(self, arg):
    super(DriverSet, self).__init__()
    self.drivers = []
    for name in arg:
      self.drivers.append(Driver(name))
    self.index = 0
  def addDriver(self,driver):
    self.drivers.append(driver)
    self.index+=1
  def __str__(self):
    return ", ".join([str(n) for n in self.drivers])
  def next(self):
      if self.index == len(self.drivers):
          raise StopIteration
      self.index+=1
      return self.drivers[self.index-1]
  def __iter__(self):
      self.index=0
      return self


drivers=DriverSet(['Nate','Matt','Kersing','Ethan','Chen','Vicky','Natalie','Derek','Gary','Kyle','Wences','Michael','Grace','Vivien','Dan','Jonathan','Andrew'])

class RideSet(object):
  """docstring for RideSet"""
  def __init__(self, date):
    super(RideSet, self).__init__()
    self.date = date
    self.drivers = DriverSet([])
  def addDriver(self,driver):
    if driver not in self.drivers:
      self.drivers.addDriver(driver)
  def printDrivers(self):
    print self.drivers

def findDriver(s):
  for driver in drivers:
    if str(driver) in s:
      return driver
  return None

def parseMessage(s, rides):
  if (len(s)==0) or ("</b>" not in s):
    return rides
  start = s.index('<b')
  end = s.index('</b>')
  # parser = HTMLParser()
  # print parser.unescape(s[start+3:end])
  d = findDriver(s[start+3:end])
  if d:
    rides.addDriver(d)
    d.addRide(rides.date)
  try:
    parseMessage(s[end+3:], rides)
  except ValueError:
    print s
    raise

def icforsunday(d):
    daystosunday = 6 - d.weekday()
    if daystosunday <= 0: # Target day already happened this week
        daystosunday += 7
    daystofriday = 4 - d.weekday()
    if daystofriday <= 0: # Target day already happened this week
        daystofriday += 7
    return d + timedelta(min(daystofriday,daystosunday))

ridesmail = mbox("ICF Rides.mbox")

# print drivers
# for d in drivers:
#   print d

for mail in ridesmail:
  print mail['date']
  if mail.is_multipart():
    content = ''.join(part.get_payload(decode=True) for part in mail.get_payload()[1:])
  else:
    content = mail.get_payload(decode=True)

  # parse date
  dateline = mail['date'][:mail['date'].find("201")+4]
  try:
    d = datetime.strptime(dateline,"%a, %d %b %Y")
    print d.__format__("%a %m/%d")
  except ValueError:
    try:
      d = datetime.strptime(dateline,"%a, %b %d, %Y")
      print d
    except ValueError:
      try:
        d = datetime.strptime(dateline,"%b %d, %Y")
        print d
      except:
        print "Error", dateline
        continue
  # align date with closest friday or sunday
  d = icforsunday(d)
  r = RideSet(d)
  parseMessage(content,r)
  r.printDrivers()

for d in drivers:
  print d,":", d.rideCount()