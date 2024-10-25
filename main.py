from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# MySQL database URL with blank password
DATABASE_URL = "mysql+pymysql://root:@localhost/oyly"

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app instance
app = FastAPI()

# Define User model
class User(Base):
    __tablename__ = "contact_us"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    email_id = Column(String(100), unique=True, index=True)
    mobile_no = Column(String(100), unique=True, index=True)
    message = Column(String(100), unique=True, index=True)
    date = Column(String(100), unique=True, index=True)

# Create the table in the database (run only once)
Base.metadata.create_all(bind=engine)

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to retrieve a user by ID
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email_id,"mobile": user.mobile_no,"message": user.message,"date": user.date}

# Route to retrieve all users
@app.get("/users", response_model=list[dict])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "name": user.name, "email": user.email_id,"mobile": user.mobile_no,"message": user.message,"date": user.date} for user in users]
