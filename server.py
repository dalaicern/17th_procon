from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from typing import Any, Dict
from problem import Problem
from datetime import datetime, timezone, timedelta
from team import Team
import time
import threading
import asyncio


# size of field
N = 4
start_time = int(datetime.now().timestamp())
lock = threading.Lock()

app = FastAPI(
    title="Simple Competition Backend",
    description="""
## Competition Backend API
This backend provides three main endpoints:

### **1. `/register`**
Register a team and receive a JWT token for authentication.

### **2. `/problem`**
Validate the token and return new problem generated randomly. This problem is based on above parameters.

### **3. `/submit`**
Submit problem data under the authenticated team.

Tokens expire after **1 day**.
""",
)
security = HTTPBearer()

SECRET_KEY = "8Wu6WztGqkrswHSqbqLvyD3GAfEeXF0C"  # change in production
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 1

registered_users = {}
submissions = {}

p = Problem(N, start_time, 1)

class RegisterReq(BaseModel):
    name: str = Field(..., example="Team Alpha")
    name: str

class Op(BaseModel):
    x: int = Field(..., example=0)
    y: int = Field(..., example=0)
    n: int = Field(..., example=2)

class SubmitReq(BaseModel):
    ops: list[Op] = Field(..., example=[{"x":0, "y":0, "n":2}])

async def print_scoreboard():
    while True:
        scoreboard = [(k, v[0], -v[1]) for k, v in p.teams.items()]
        scoreboard = sorted(scoreboard, key = lambda x: (x[1], x[2]), reverse = True)
        print('==================================================')
        for i, x in enumerate(scoreboard):
            print(str(i+1) + '. ' + x[0], x[1], -x[2])
        print('==================================================')
        await asyncio.sleep(10)  # Run every 10 seconds

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(print_scoreboard())
    
def create_token(name: str):
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    payload = {"name": name, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validate_token(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["name"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/register", summary="Register a new team", description="Registers a team and returns a JWT token.")
def register(req: RegisterReq):
    token = create_token(req.name)
    lock.acquire()
    test = req.name not in registered_users
    lock.release()
    if test:
        registered_users[req.name] = Team(req.name, token, p)
    else:
        return {"Team is already registered"}
    return {"token": token}

@app.get("/problem", summary="Get owner info", description="Checks token validity and returns the team name associated with it.")
def problem(credentials: HTTPAuthorizationCredentials = Depends(security)):
    name = validate_token(credentials)
    return str(p)

@app.post("/submit", summary="Submit solution", description="Stores a submission for the authenticated team.")
def submit(req: SubmitReq, credentials: HTTPAuthorizationCredentials = Depends(security)):
    now = datetime.now()
    deadline = datetime.fromtimestamp(start_time) + timedelta(minutes = 5)
    if now > deadline:
        return {'Problem ended'}
    name = validate_token(credentials)
    lock.acquire()
    test = name not in registered_users
    lock.release()
    if test:
        return {"User " + name + " is not registered"}
    score, submission_time = registered_users[name].submit(req)
    return {"score": score, "submission_time": submission_time}
