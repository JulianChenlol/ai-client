from fastapi import APIRouter, HTTPException, status

from app.models import PrimaryKey
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import PostCreate, PostRead, PostUpdate, PostPagination
from .service import create, get, update, delete

router = APIRouter()


@router.get("", response_model=PostPagination)
def get_all_posts(common: CommonParameters):
    """Get all Posts"""
    return search_filter_sort_paginate(model="Post", **common)


@router.post("", response_model=PostCreate)
def create_post(db_session: DbSession, post_in: PostCreate):
    """Create a new Post"""
    return create(db_session=db_session, post_in=post_in)


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
    return update(db_session=db_session, post=post, post_in=post_in)


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
