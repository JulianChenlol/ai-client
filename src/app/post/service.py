from typing import Optional, List
from sqlalchemy.orm import Session

from .schemas import Post
from .models import PostCreate, PostUpdate

from app.poll import service as poll_service


def get(*, db_session: Session, post_id: int) -> Optional[Post]:
    """Returns a Post object based on the given the id"""
    return db_session.query(Post).filter(Post.id == post_id).first()


def get_all(*, db_session: Session) -> List[Optional[Post]]:
    """Returns all  Post objects"""
    return db_session.query(Post).all()


def create(*, db_session: Session, post_polls_in: PostCreate) -> Post:
    """Creates a new Post object"""
    with db_session.begin():
        create_data = post_polls_in.model_dump(exclude={"polls"})
        post = Post(**create_data)
        db_session.add(post)
        db_session.flush()
        if post_polls_in.polls:
            for post_poll in post_polls_in.polls:
                post_poll.poll.post_id = post.id
                poll_service.create_or_update(db_session=db_session, poll_in=post_poll.poll)
        db_session.commit()
    return post


def update(*, db_session: Session, post: Post, post_polls_in: PostUpdate) -> Post:
    """Updates a Post object"""
    with db_session.begin():
        post_data = post.dict()
        update_data = post_polls_in.model_dump(exclude={"polls"})
        for field in post_data:
            if field in update_data:
                setattr(post, field, update_data[field])
        if post_polls_in.polls:
            for post_poll in post_polls_in.polls:
                if post_poll.poll.id:
                    poll_service.create_or_update(db_session=db_session, poll_in=post_poll.poll)
        db_session.commit()
    return post


def delete(*, db_session: Session, post_id: int) -> bool:
    """Deletes a Post object"""
    post = db_session.query(Post).filter(Post.id == post_id).first()
    db_session.delete(post)
    db_session.commit()
    return True


def get_by_user(*, db_session: Session, user_id: int) -> List[Optional[Post]]:
    """Returns all Post objects by user"""
    return db_session.query(Post).filter(Post.user_id == user_id).all()
