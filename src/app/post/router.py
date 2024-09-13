from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models import PrimaryKey
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import PostCreate, PostRead, PostUpdate, PostPagination
from .service import create, get, update, delete

from app.poll.service import get_by_post
from app.poll.models import PollRead

router = APIRouter()


@router.get("", response_model=PostPagination)
def get_all_posts(common: CommonParameters):
    """Get all Posts"""
    return search_filter_sort_paginate(model="Post", **common)


@router.post("", response_model=PostRead)
def create_post(db_session: DbSession, post_in: PostCreate):
    """Create a new Post"""
    return create(db_session=db_session, post_polls_in=post_in)


@router.get("/{post_id}", response_model=PostRead)
def get_post(db_session: DbSession, post_id: int):
    """Get a Post"""
    return get(db_session=db_session, post_id=post_id)


@router.put("/{post_id}", response_model=PostRead)
def update_post(db_session: DbSession, post_id: PrimaryKey, post_in: PostUpdate):
    """Update a Post"""
    post = get(db_session=db_session, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Post with this id does not exist."}],
        )
    return update(db_session=db_session, post=post, post_polls_in=post_in)


@router.delete("/{post_id}")
def delete_post(db_session: DbSession, post_id: int):
    """Delete a Post"""
    post = get(db_session=db_session, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Post with this id does not exist."}],
        )
    delete(db_session=db_session, post_id=post_id)


@router.get("/{post_id}/polls", response_model=List[PollRead])
def get_polls_by_post(db_session: DbSession, post_id: int):
    """Get all Polls by Post"""
    return get_by_post(db_session=db_session, post_id=post_id)
