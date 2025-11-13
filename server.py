from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from typing import Any, Dict
from problem import Problem
from datetime import datetime, timezone


# size of field
N = 10
start_time = datetime.now()

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

class SubmitReq(BaseModel):
    data: dict = Field(..., example={"answer": "42", "problem_id": 1})
    data: dict

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
    registered_users[token] = req.name
    return {"token": token}

@app.get("/problem", summary="Get owner info", description="Checks token validity and returns the team name associated with it.")
def problem(credentials: HTTPAuthorizationCredentials = Depends(security)):
    name = validate_token(credentials)
    return str(p)

@app.post("/submit", summary="Submit solution", description="Stores a submission for the authenticated team.")
def submit(req: SubmitReq, credentials: HTTPAuthorizationCredentials = Depends(security)):
    name = validate_token(credentials)
    if name not in submissions:
        submissions[name] = []
    submissions[name].append(req.data)
    return {"status": "saved", "owner": name}
