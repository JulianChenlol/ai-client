from typing import Optional, List
from sqlalchemy.orm import Session

from .schemas import Poll
from .models import PollCreate, PollUpdate, PollRead


def get(*, db_session: Session, poll_id: int) -> Optional[Poll]:
    """Returns a Poll object based on the given the id"""
    return db_session.query(Poll).filter(Poll.id == poll_id).first()


def get_by_post(*, db_session: Session, post_id: int) -> List[Optional[Poll]]:
    """Returns all Poll objects by post"""
    return db_session.query(Poll).filter(Poll.post_id == post_id).order_by(Poll.order).all()


def create(*, db_session: Session, poll_in: PollCreate) -> Poll:
    """Creates a new Poll object"""
    poll = Poll(**poll_in.model_dump())
    db_session.add(poll)
    db_session.commit()
    return poll


def update(*, db_session: Session, poll: Poll, poll_in: PollUpdate) -> Poll:
    """Updates a Poll object"""
    poll_data = poll.dict()
    update_data = poll_in.model_dump(exclude_unset=True)
    for field in poll_data:
        if field in update_data:
            setattr(poll, field, update_data[field])
    db_session.commit()
    return poll


def create_or_update(*, db_session: Session, poll_in: PollRead) -> Poll:
    """[session no commit] Creates or Updates a Poll object"""
    poll = get(db_session=db_session, poll_id=poll_in.id)
    if poll:
        poll_data = poll.dict()
        update_data = poll_in.model_dump(exclude_unset=True)
        for field in poll_data:
            if field in update_data:
                setattr(poll, field, update_data[field])
    else:
        poll = Poll(**poll_in.model_dump())
        db_session.add(poll)
    return poll


def delete(*, db_session: Session, poll_id: int):
    """Deletes a Poll object"""
    poll = db_session.query(Poll).filter(Poll.id == poll_id).first()
    db_session.delete(poll)
    db_session.commit()
