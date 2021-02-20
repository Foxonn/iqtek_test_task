from typing import Union, Optional, List
import sys

import uvicorn
from fastapi import FastAPI, Query, HTTPException

from app.usermanager.schemas import User, UserOutput, UserPartialUpdate
from app.usermanager import services
from app.usermanager.storage.exceptions import StorageException, ItemNotFound

app = FastAPI()


@app.get("/", response_model=List[UserOutput])
def get_all_users_():
    return services.get_all_users()


@app.post("/", response_model=UserOutput)
def add_user(user: User):
    return services.add_user(user)


@app.get("/user/{user_id}", response_model=User)
def get_user_(user_id: Union[int, str]):
    try:
        return services.get_user_by_id(user_id)
    except ItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@app.put("/user/{id}", response_model=User)
def update_user_(id: Union[int, str], user: User):
    try:
        return services.update_user(id, user)
    except ItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@app.patch("/user/{id}", response_model=UserPartialUpdate)
def partial_update_user(id: Union[int, str], user: UserPartialUpdate):
    try:
        return services.partial_update_user(id, user)
    except ItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@app.delete("/user/{id}")
def delete_user(id: Union[int, str]):
    try:
        services.delete_user(id)
        return {'detail': True}
    except ItemNotFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


if __name__ == '__main__':
    uvicorn.run("app.usermanager.main:app", host='localhost', port=8000)
