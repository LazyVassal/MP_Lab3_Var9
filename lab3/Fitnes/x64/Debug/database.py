from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, date

# Настройка подключения к SQLite БД
DATABASE_URL = "sqlite:///fitness_club.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    
    # Связи
    memberships = relationship("Membership", back_populates="client")
    trainings = relationship("Training", back_populates="client")

class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    type = Column(String(50), nullable=False) # e.g., 'Monthly', 'Yearly'
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Связи
    client = relationship("Client", back_populates="memberships")

class Training(Base):
    __tablename__ = "trainings"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    training_date = Column(DateTime, default=datetime.utcnow)
    activity = Column(String(50), nullable=False) # e.g., 'Yoga', 'Gym'
    
    # Связи
    client = relationship("Client", back_populates="trainings")

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# --- CRUD Операции ---

def create_client(session, name, phone, email):
    new_client = Client(name=name, phone=phone, email=email)
    session.add(new_client)
    session.commit()
    return new_client

def create_membership(session, client_id, type, start_date, end_date):
    new_membership = Membership(
        client_id=client_id,
        type=type,
        start_date=start_date,
        end_date=end_date
    )
    session.add(new_membership)
    session.commit()
    return new_membership

def create_training(session, client_id, activity):
    new_training = Training(client_id=client_id, activity=activity)
    session.add(new_training)
    session.commit()
    return new_training

def get_client_by_id(session, client_id):
    return session.query(Client).filter(Client.id == client_id).first()

def get_all_clients(session):
    return session.query(Client).all()

def update_client(session, client_id, **kwargs):
    client = get_client_by_id(session, client_id)
    if client:
        for key, value in kwargs.items():
            setattr(client, key, value)
        session.commit()
        return True
    return False

def delete_client(session, client_id):
    client = get_client_by_id(session, client_id)
    if client:
        session.delete(client)
        session.commit()
        return True
    return False

# --- Поисковые запросы ---

def get_active_memberships(session):
    today = date.today()
    return session.query(Membership).filter(
        Membership.start_date <= today,
        Membership.end_date >= today
    ).all()

def get_client_trainings_history(session, client_id):
    return session.query(Training).filter(Training.client_id == client_id).order_by(Training.training_date.desc()).all()