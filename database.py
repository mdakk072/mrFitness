from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence,ForeignKey
from sqlalchemy.orm import relationship

Base=declarative_base()
class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)
        
    def add_user(self, user):
        session = self.SessionLocal()
        try:
            session.add(user)
            session.commit()
        except:
            session.rollback()
            print('Erreur : utilisateur')

    def add_day(self, day):
        session = self.SessionLocal()
        try:
            session.add(day)
            session.commit()
        except:
            session.rollback()
            print('Erreur : ajout day')
    
    def get_user(self, username):
        session = self.SessionLocal()
        user = session.query(User).filter(User.username == username).first()
        return user

    def createUser(self,user):
        #user = User("John Doe", "johndoe", "password123", "johndoe@example.com", 80, 180, "kg")
        self.add_user(user)
        day = Day(f"{randint(1992,2023)}-{randint(1,12)}-{randint(1,30)}", user.id)
        self.add_day(day)
    def getUserInfos(self,username):
        user=self.get_user(username)
        print('>>>',user)
        for day in user.days:
            print(">",day.date)
    def addDayForUser(self,user,day='01-01-00'):
        dayToAdd = Day(day, user.id)
        self.add_day(dayToAdd)
    def get_all_users(self):
        session = self.SessionLocal()
        users = session.query(User).all()
        return users



    
    # Récupération de l'utilisateur


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    mail = Column(String)
    poids = Column(Integer)
    taille = Column(Integer)
    unite = Column(String)
    days = relationship("Day", backref="user")
    
    def __init__(self, nom,username,password,mail, poids, taille, unite):
        self.nom = nom
        self.username = username
        self.password = password
        self.mail = mail
        self.poids = poids
        self.taille = taille
        self.unite = unite
    def __repr__(self) -> str:
        return f"{self.id}|{self.nom}|{self.username}|{self.mail}|{self.poids},{self.taille},{self.unite}"


class Day(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    user_id=Column(Integer,ForeignKey('users.id'))

    def __init__(self, date, user_id):
        self.date = date
        self.user_id = user_id

def test_db0(db_url):
    # Initialisation de la base de données
    db = Database(db_url)
    db.init_db()
    user = User("John Doe", "johndoe", "password123", "johndoe@example.com", 80, 180, "kg")
    db.createUser(user)
    # Création d'un utilisateur
    db.getUserInfos(user.username)
    #retrieved_user = db.get_user(user.username)

    
    # Récupération des jours pour l'utilisateur
    #retrieved_days = retrieved_user.days
    #print("Retrieved days:", retrieved_days[0].date)

# Utilisation de la fonction de test avec l'URL de votre base de données
    



def test_db(db_url):
    # Initialisation de la base de données
    db = Database(db_url)
    db.init_db()

    # Création de 100 utilisateurs
    for i in range(100):
        user = User(f"User {i}", f"user{i}", f"passr{randint(1,1000)}", f"user{randint(34,4363)}@example.com", randint(48,150), randint(150,192), "kg")
        db.createUser(user)
    
    for i in range (1000):
        tt=randint(0,1)

        if tt : 
            user=db.get_user(f'user{randint(0,99)}')
            didi=f"{randint(1992,2023)}-{randint(1,12)}-{randint(1,30)}"
            db.addDayForUser(user,didi)

    for i in range(100):
        db.getUserInfos(f'user{i}')
        print('=--------------------------0')
    
     

# Utilisation de la fonction de test avec l'URL de votre base de données
test_db("sqlite:///test.db")


