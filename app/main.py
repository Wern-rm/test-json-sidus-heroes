import os
import secrets

import aioredis
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.crud import create_new_user, get_user_by_login, get_user_by_id, update_db_user
from app.database import Base, engine, SessionLocal
from app.schemas import UserCreate, UserUpdate

# Create DB
Base.metadata.create_all(bind=engine)
# Create REST-API
app = FastAPI(title='Sidus-Heroes Test json REST-API')
# Create security settings
security = HTTPBasic()


def configure_redis() -> str:
    """
    Config Redis DB
    """
    redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
    redis_port = os.environ.get('REDIS_PORT', '6379')
    redis_password = os.environ.get('REDIS_PASSWORD', '')
    return f'redis://{redis_password}@{redis_host}:{redis_port}/1'


# Create Redis Session
redis = aioredis.from_url(configure_redis())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_auth(credentials: HTTPBasicCredentials = Depends(security),
               db: Session = Depends(get_db)):
    auth_user = get_user_by_login(db=db, login=credentials.username)
    # Check user DB select
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password"
        )
    # Check user password in DB
    if not secrets.compare_digest(credentials.password, auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password"
        )
    return auth_user.id


@app.get("/")
async def index():
    return {"message": "Sidus-Heroes test job API"}


@app.get("/get/user/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    # Check cache user
    cache_user = await redis.hgetall(f'user-{id}')
    if cache_user:
        return cache_user

    db_user = get_user_by_id(db, id=id)
    # Check db select
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found.")

    # Create cache
    await redis.hset(f'user-{id}', mapping={'login': db_user.login, 'name': db_user.name, 'create_date': str(db_user.at_create)})
    return {'login': db_user.login, 'name': db_user.name, 'create_date': db_user.at_create}


@app.post("/create/user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_login(db, login=user.login)
    # Check user select
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login already registered")
    new_user_id = create_new_user(db=db, login=user.login, password=user.password, name=user.name)
    # Check create result
    if new_user_id == -1:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="System error")
    return {'message': 'Success create user.', 'user_id': new_user_id}


@app.put("/update/user/{id}")
async def update_user(id: int, user: UserUpdate,
                      db: Session = Depends(get_db),
                      user_id_auth: str = Depends(check_auth)):
    # Check usage ID for auth ID
    if user_id_auth != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password"
        )

    db_user = get_user_by_id(db, id=id)
    # Check user select
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found.")
    result = update_db_user(db=db, user_id=id, new_login=user.new_login, new_name=user.new_name)
    # Check update
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="System error")

    # Remove cache for user ID
    await redis.delete(f'user-{id}')
    return {'message': 'Success update user', 'user_id': id}


