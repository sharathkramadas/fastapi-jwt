import os
from fastapi import FastAPI, Request, HTTPException, Depends
from typing import Optional
import uvicorn
import jwt
import bcrypt
from pydantic import BaseModel
from crud.models import User, SessionLocal, engine, Base
from sqlalchemy.orm import Session

app = FastAPI()

SECRET = os.environ.get('JWT_PASS','secret')

Base.metadata.create_all(bind=engine)

class Credentials(BaseModel):
	email: str
	password: str

class UserData(BaseModel):
	first_name: str	
	last_name: str
	email: str	
	password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()			

@app.post('/users/create')
def create_user(data: UserData, db: Session = Depends(get_db)):	
	user = User()
	user.first_name = data.first_name
	user.last_name = data.last_name
	user.email = data.email
	hashed = bcrypt.hashpw(data.password.encode('utf8'), bcrypt.gensalt())	
	user.password = hashed
	db.add(user)
	db.commit()
	db.refresh(user)
	return {"message":"User data saved successfully!"}		

@app.post('/login')
def login(data: Credentials, db: Session = Depends(get_db)):	
	user = db.query(User).filter(User.email == data.email).first()
	if user:					
		if bcrypt.checkpw(data.password.encode('utf8'), user.password):
			claims = {
				"email":data.email
			}
			token = jwt.encode(claims,SECRET,algorithm="HS256")
			return {"token":token}
		else:
			raise HTTPException(status_code=403, detail="Invalid credentials!")
	else:
		raise HTTPException(status_code=403, detail="Invalid credentials!")

@app.get('/verify')
def verify(request: Request, db: Session = Depends(get_db)):
	token = request.headers.get("Authorization")
	claims = jwt.decode(token,SECRET,algorithms=["HS256"])
	email = claims.get('email')	
	user = db.query(User).filter(User.email == email).first()
	if user:					
		return {"message":"Token validated successfully!"}	
	else:
		raise HTTPException(status_code=403, detail="Invalid token!")

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')	