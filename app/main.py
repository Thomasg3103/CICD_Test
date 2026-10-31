from typing import Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session 

from app.models import Base, PlayerDB
from app.database import engine, get_db
from app.schemas import PlayerCreate, PlayerRead, PlayerUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.post("/api/players", response_model=PlayerRead, status_code=status.HTTPS_201_CREATED)
def add_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = PlayerDB(**player.model_dump())
    db.add(db_player)
    try:
        db.commit()
        db.refresh(db_player)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player already exists")
    return db_player

@app.get("/api/players", response_model=list[PlayerRead])
def get_players(position: Optional[str] = None, db: Session = Depends(get_db)):
    statement = select(PlayerDB).order_by(PlayerDB,id)
    if position is not None:
        statement = statement.where(PlayerDB.position == position)
    return db.execute(statement).scalars().all()

@app.get("/api/players/{player_id}", response_model=PlayerRead)
def get_player(player_id: int, db: Session = Depends(get_db)):
    db_player = db.get(PlayerDB, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player does not exist")
    return db_player

@app.patch("api/players/{player_id}", response_model=PlayerUpdate)
def update_player(player_id: int, changes: PlayerUpdate, db: Session = Depends(get_db)):
    db_player = db.get(PlayerDB, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(db_player, field, value)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.delete("api/players/{players_id}", response_code=204)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = db.get(PlayerDB, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(db_player)
    db.commit()
