from fastapi import APIRouter, HTTPException, status

from app.models import PrimaryKey
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import PollCreate, PollRead, PollUpdate, PollPagination
from .service import create, get, update, delete


router = APIRouter()


@router.get("", response_model=PollPagination)
def get_all_polls(common: CommonParameters):
    """Get all Polls"""
    return search_filter_sort_paginate(model="Poll", **common)


@router.post("", response_model=PollCreate)
def create_poll(db_session: DbSession, poll_in: PollCreate):
    """Create a new Poll"""
    return create(db_session=db_session, poll_in=poll_in)


@router.get("/{poll_id}", response_model=PollRead)
def get_poll(db_session: DbSession, poll_id: int):
    """Get a Poll"""
    return get(db_session=db_session, poll_id=poll_id)


@router.put("/{poll_id}", response_model=PollRead)
def update_poll(db_session: DbSession, poll_id: PrimaryKey, poll_in: PollUpdate):
    """Update a Poll"""
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Poll with this id does not exist."}],
        )
    return update(db_session=db_session, poll=poll, poll_in=poll_in)


@router.delete("/{poll_id}")
def delete_poll(db_session: DbSession, poll_id: int):
    """Delete a Poll"""
    poll = get(db_session=db_session, poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Poll with this id does not exist."}],
        )
    delete(db_session=db_session, poll_id=poll_id)
