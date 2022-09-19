from datetime import date
import random
import sqlite3
con = sqlite3.connect('Kaffe.db')

cur = con.cursor()

loggedIn = ""

def reset():
  cur.execute("DROP TABLE IF EXISTS Bruker")
  cur.execute("DROP TABLE IF EXISTS ForedlingsMetode")
  cur.execute("DROP TABLE IF EXISTS Gaard")
  cur.execute("DROP TABLE IF EXISTS GaardDyrker")
  cur.execute("DROP TABLE IF EXISTS Kaffe")
  cur.execute("DROP TABLE IF EXISTS KaffeSmaking")
  cur.execute("DROP TABLE IF EXISTS Parti")
  cur.execute("DROP TABLE IF EXISTS PartiBestaarAv")
  cur.execute("DROP TABLE IF EXISTS Region")

  cur.execute(""" 
  CREATE TABLE Region(
    ID		INTEGER NOT NULL,
  RegionNavn	TEXT NOT NULL,
  Land		TEXT NOT NULL,
  CONSTRAINT IDPK PRIMARY KEY (ID));
  """)

  insert("Region", (1, "Santa Ana", "El Salvador"))
  insert("Region", (2, "Santa Ana", "Rwanda"))
  insert("Region", (3, "Santa Ana", "Colombia"))



  cur.execute("""
  CREATE TABLE Gaard(
  ID		INTEGER NOT NULL,
  Navn		TEXT NOT NULL,
  Moh		INTEGER,
  RegionID	INTEGER,
  CONSTRAINT IDPK PRIMARY KEY (ID),
  CONSTRAINT RegionIDFK FOREIGN KEY (RegionID) REFERENCES Region(ID)
    ON UPDATE CASCADE
    ON DELETE SET NULL);
  """)

  insert("Gaard", (1, "Nombre de Dios", 1500, 1))
  insert("Gaard", (2, "gaard2", 1500, 2))
  insert("Gaard", (3, "gaard3", 1500, 3))

  cur.execute("""
  CREATE TABLE GaardDyrker(
  GaardID		INTEGER NOT NULL,
  KaffeBonneArt	TEXT NOT NULL,
  CONSTRAINT GaardIDFK FOREIGN KEY (GaardID) REFERENCES Gaard(ID)
  ON UPDATE CASCADE
  ON DELETE CASCADE);
  """)

  insert("GaardDyrker", (1, "Burbon"))
  insert("GaardDyrker", (1, "Liberica"))

  cur.execute("""
  CREATE TABLE ForedlingsMetode(
  Navn		TEXT NOT NULL,
  Beskrivelse	TEXT,
  CONSTRAINT NavnPK PRIMARY KEY (Navn));
  """)

  insert("ForedlingsMetode", ("Baertorket", "Torket baer:)"))
  insert("ForedlingsMetode", ("Washed", "Med Zalo:)"))

  cur.execute("""
  CREATE TABLE Parti(
  ID		INTEGER NOT NULL,
  GaardID		INTEGER,
  BetaltPrKG	REAL NOT NULL,
  InnhøstingsAar	INTEGER NOT NULL,
  ForedlingsMetode TEXT NOT NULL,
  CONSTRAINT IDPK PRIMARY KEY (ID),
  CONSTRAINT GaardIDFK FOREIGN KEY (GaardID) REFERENCES Gaard(ID)
    ON UPDATE CASCADE
    ON DELETE SET NULL,
  CONSTRAINT ForedlingsMetodeFK FOREIGN KEY (ForedlingsMetode) REFERENCES ForedlingsMetode(navn));
  """)

  insert("Parti", (1, 1, 8.0, 2021, "Baertorket"))
  insert("Parti", (2, 2, 8.0, 2021, "Washed"))
  insert("Parti", (3, 3, 8.0, 2021, "Baertorket"))

  cur.execute("""
  CREATE TABLE PartiBestaarAv(
  PartiID		INTEGER NOT NULL,
  KaffeBonneArt TEXT NOT NULL,
  CONSTRAINT PartiIDFK FOREIGN KEY (PartiID) REFERENCES Parti(ID)
    ON UPDATE CASCADE
    ON DELETE SET NULL);
  """)

  insert("PartiBestaarAv", (1, "Bourbon"))

  cur.execute("""
  CREATE TABLE Kaffe(
    PartiID		INTEGER NOT NULL,
    Navn		TEXT NOT NULL,
    Beskrivelse	TEXT NOT NULL,
    PrisPrKG	REAL NOT NULL,
    Brenneri		TEXT NOT NULL,
    BrenningsGrad	TEXT NOT NULL,
    BrenningsDato 		DATE NOT NULL,
    CONSTRAINT PartiIDPK PRIMARY KEY (PartiID),
    CONSTRAINT PartiIDFK FOREIGN KEY (PartiID) REFERENCES Parti(ID)
    ON UPDATE CASCADE
    ON DELETE CASCADE);
  """)

  insert("Kaffe", (1, "Vinterkaffe 2022", "En velsmakende og kompleks kaffe for morketiden", 600, "Jacobsen & Svart", "lysbrent", "2022-01-20"))
  insert("Kaffe", (2, "Vinterkaffe 2023", "En velsmakende og floral kaffe for morketiden", 600, "Jacobsen & Svart", "lysbrent", "2023-01-20"))
  insert("Kaffe", (3, "Vinterkaffe 2024", "En velsmakende og kompleks kaffe for morketiden", 600, "Jacobsen & Svart", "lysbrent", "2024-01-20"))


  cur.execute("""
  CREATE TABLE Bruker(
    Navn		TEXT NOT NULL,
    Epost		TEXT NOT NULL,
    Passord		TEXT NOT NULL,
    CONSTRAINT IDPK PRIMARY KEY (Epost));
  """)

  insert("Bruker", ("navn", "epost", "passord"))
  insert("Bruker", ("navn2", "epost2", "passord2"))
  insert("Bruker", ("navn3", "epost3", "passord3"))
  insert("Bruker", ("navn4", "epost4", "passord4"))

  cur.execute("""
  CREATE TABLE KaffeSmaking(
    ID		NUMERIC NOT NULL,
    BrukerEpost		TEXT NOT NULL,
    PartiID		NUMERIC NOT NULL,
    SmaksNotater	TEXT,
    Dato		DATE NOT NULL,
    Poeng		NUMERIC NOT NULL,
    CONSTRAINT IDPK PRIMARY KEY (ID),
    CONSTRAINT BrukerEpostFK FOREIGN KEY (BrukerEpost) REFERENCES Bruker(Epost)
    ON UPDATE CASCADE
      ON DELETE CASCADE,
    CONSTRAINT PartiIDFK FOREIGN KEY (PartiID) REFERENCES Kaffe(PartiID)
    ON UPDATE CASCADE
    ON DELETE CASCADE);
  """)

  insert("KaffeSmaking", (123456, "epost", 1, "Quite shite", date.today(), 10))
  insert("KaffeSmaking", (11256, "epost", 1, "Quite shite", date.today(), 8))
  insert("KaffeSmaking", (654321, "epost2", 1, "Quite shite", date.today(), 9))
  insert("KaffeSmaking", (1221, "epost2", 3, "Quite shite", "2020-01-20", 1))
  insert("KaffeSmaking", (153763, "epost3", 1, "Quite shite", "2023-01-20", 5))
  insert("KaffeSmaking", (1163, "epost3", 2, "Quite shite", date.today(), 2))
  insert("KaffeSmaking", (153563, "epost3", 3, "Quite shite", date.today(), 10))

def insert(table, args):
  questionmarks = "(?"
  for i in range(len(args)-1):
    questionmarks += ", ?"
  questionmarks += ");"
  con.execute("INSERT INTO " + table + " VALUES " + questionmarks, args)

def register():
  valid = False
  while not valid:
    email = input("Enter email:\n")
    cur.execute("SELECT Epost FROM Bruker WHERE Epost = ?", (email, ))
    valid = cur.fetchone() == None
    if(email == "exit"):
      return
    if(not valid):
      print("That email is already in use, enter another. To go back, type exit")
  password = input("Enter password:\n")
  valid = False
  while not valid:
    name = input("Enter full name:\n")
    valid = len(name) > 1
    if(email == "exit"):
      return
    if(not valid):
      print("That username is too short, enter another. To go back, type exit")
  insert("Bruker", (name, email, password))

  cur.execute("SELECT Navn FROM Bruker WHERE Epost = ?", (email, ))
  print(str(cur.fetchone()[0]) + " successfully registered")

def login():
  global loggedIn
  email = input("Enter email: ")
  cur.execute("SELECT Passord FROM Bruker WHERE Epost = ?", (email,))
  DBpassword = cur.fetchone()
  if DBpassword != None:
    password = input("Enter password: ")
    if password == DBpassword[0]:
      loggedIn = email
      print("Logged in as "+email)
    else:
      print("Incorrect password")
  else:
    print("Email not found")
  return

def logout():
  global loggedIn
  if loggedIn != "":
    loggedIn = ""
    print("Logged out")
  else:
    print("Not logged in")
  return

def insertKaffeSmaking():
  global loggedIn
  if loggedIn == "":
    print("Not logged in")
    return

  name = input("Enter coffee name: ")
  roastery = input("Enter roastery: ")
  roastingDate = input("Enter roasting date: ")

  cur.execute("SELECT PartiID FROM Kaffe WHERE Navn = ? AND Brenneri = ? AND BrenningsDato = ?;", (name, roastery, roastingDate))
  PartiID = cur.fetchone()
  if PartiID == None:
    print("Coffee not found")
    return
  
  validPoints = False
  while not validPoints:
    points = int(input("Enter rating from 1 to 10: "))
    validPoints = points > 0 and points < 11
    if(not validPoints):
      print("Points must be an integer from 1 to 10.")
  tasteNotes = input("Enter taste notes: ")

  insert("KaffeSmaking", (random.randint(1,1000000), loggedIn, PartiID[0], tasteNotes, date.today(), points))

def scoreboard():
  cur.execute("""SELECT Bruker.Navn, COUNT(DISTINCT Kaffe.PartiID) FROM Bruker 
    JOIN KaffeSmaking ON Bruker.Epost = KaffeSmaking.BrukerEpost
    JOIN Kaffe ON KaffeSmaking.PartiID = Kaffe.PartiID
    WHERE strftime('%Y', KaffeSmaking.Dato) = strftime('%Y', 'now')
    GROUP BY Bruker.Navn 
    ORDER BY COUNT(DISTINCT Kaffe.PartiID) DESC;
  """)

  counter = 1
  for row in cur.fetchall():
    print("In " + str(counter) + ". place: " + row[0] + " with " + str(row[1]) + " tastings")
    counter+=1

def costEffective():
  cur.execute("""SELECT Kaffe.Navn, Kaffe.Brenneri, Kaffe.PrisPrKG, AVG(KaffeSmaking.Poeng) FROM Kaffe 
    JOIN KaffeSmaking ON Kaffe.PartiID = KaffeSmaking.PartiID
    GROUP BY Kaffe.PartiID 
    ORDER BY AVG(KaffeSmaking.Poeng)/Kaffe.PrisPrKG DESC;
  """)

  counter = 1
  for row in cur.fetchall():
    print("In " + str(counter) + ". place: " + row[0] + " from " + row[1] + " for " + str(row[2]) + " a kilo, averaging a score of " + str(row[3]))
    counter+=1

def sok():
  where = ""
  arguments = []
  sokeord = input("Enter something to search by(optional): ")
  if sokeord:
    where += "(Kaffe.Beskrivelse LIKE ? OR KaffeSmaking.SmaksNotater LIKE ?) "
    arguments.append('%'+sokeord+'%')
    arguments.append('%'+sokeord+'%')


  land = input("Enter countries of origin(optional): ")
  if land:
    land = land.split(", ")
    if where:
      where += "AND " 
    where += "("
    where += "Region.Land LIKE ?"
    arguments.append(land[0])
    for i in range(1, len(land)):
      where += " OR Region.Land LIKE ?"
      arguments.append(land[i])
    where += ") "
  
  metode = input("Enter a processing method(optional): ")
  if metode:
    if where:
      where += "AND "
    if metode.startswith("not "):
      where += "Parti.ForedlingsMetode NOT LIKE ? "
      arguments.append(metode[4:])
    else:
      where += "Parti.ForedlingsMetode LIKE ? "
      arguments.append(metode)
  
  if not where:
    where = "1=1"

  cur.execute("""SELECT DISTINCT Kaffe.Navn, Kaffe.Brenneri FROM Kaffe 
    LEFT JOIN KaffeSmaking ON Kaffe.PartiID = KaffeSmaking.PartiID
    LEFT JOIN Parti ON Kaffe.PartiID = Parti.ID
    LEFT JOIN Gaard ON Parti.GaardID = Gaard.ID
    LEFT JOIN Region ON Gaard.RegionID = Region.ID
    WHERE """ + where, arguments)

  result = cur.fetchall()
  if len(result) > 0:
    for row in result:
      print(row[0] + " from " + row[1])
  else:
    print("No coffes match that search.")

UI = ""
while UI != "exit":
  print()
  UI = input("Enter your desired command: ")
  if UI == "reset":
    reset()
  elif UI == "register":
    register()
  elif UI == "login":
    login()
  elif UI == "logout":
    logout()
  elif UI == "insertKaffeSmaking":
    insertKaffeSmaking()
  elif UI == "scoreboard":
    scoreboard()
  elif UI == "costEffective":
    costEffective()
  elif UI == "sok":
    sok()

con.commit()
con.close()
