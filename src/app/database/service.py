from fastapi import Depends, Query
from sqlalchemy import desc, func, or_
from sqlalchemy_filters import apply_pagination, apply_sort
from sqlalchemy_filters.exceptions import BadFilterFormat, FieldNotFound
from sqlalchemy.exc import ProgrammingError
from typing import Annotated, List
import json
from pydantic_core import ValidationError, InitErrorDetails
from pydantic.types import Json, StringConstraints

from app.database.core import DbSession
from .core import get_class_by_tablename, get_model_name_by_tablename
from app.exceptions import FieldNotFoundError, InvalidFilterError
from app.utils.log_util import logger

# allows only printable characters
QueryStr = Annotated[str, StringConstraints(pattern=r"^[ -~]+$", min_length=1)]


def common_parameters(
    # current_user: CurrentUser,
    db_session: DbSession,
    page: int = Query(1, gt=0, lt=2147483647),
    items_per_page: int = Query(5, alias="itemsPerPage", gt=-2, lt=2147483647),
    query_str: QueryStr = Query(None, alias="q"),
    filter_spec: Json = Query([], alias="filter"),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
    # role: UserRoles = Depends(get_current_role),
):
    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "query_str": query_str,
        "filter_spec": filter_spec,
        "sort_by": sort_by,
        "descending": descending,
        # "current_user": current_user,
        # "role": role,
    }


CommonParameters = Annotated[
    dict[str, int | DbSession | QueryStr | Json | List[str] | List[bool]],
    Depends(common_parameters),
]


def search(*, query_str: str, query: Query, model: str, sort=False):
    """Perform a search based on the query."""
    search_model = get_class_by_tablename(model)

    if not query_str.strip():
        return query

    search = []
    if hasattr(search_model, "search_vector"):
        vector = search_model.search_vector
        search.append(vector.op("@@")(func.tsq_parse(query_str)))

    if hasattr(search_model, "name"):
        search.append(
            search_model.name.ilike(f"%{query_str}%"),
        )
        search.append(search_model.name == query_str)

    if not search:
        raise Exception(f"Search not supported for model: {model}")

    query = query.filter(or_(*search))

    if sort:
        query = query.order_by(desc(func.ts_rank_cd(vector, func.tsq_parse(query_str))))

    return query.params(term=query_str)


def create_sort_spec(model, sort_by, descending):
    """Creates sort_spec."""
    sort_spec = []
    if sort_by and descending:
        for field, direction in zip(sort_by, descending, strict=False):
            direction = "desc" if direction else "asc"

            # check to see if field is json with a key parameter
            try:
                new_field = json.loads(field)
                field = new_field.get("key", "")
            except json.JSONDecodeError:
                pass

            # we have a complex field, we may need to join
            if "." in field:
                complex_model, complex_field = field.split(".")[-2:]

                sort_spec.append(
                    {
                        "model": get_model_name_by_tablename(complex_model),
                        "field": complex_field,
                        "direction": direction,
                    }
                )
            else:
                sort_spec.append({"model": model, "field": field, "direction": direction})
    logger.debug(f"Sort Spec: {json.dumps(sort_spec, indent=2)}")
    return sort_spec


def search_filter_sort_paginate(
    db_session,
    model,
    query_str: str = None,
    filter_spec: List[dict] = None,
    page: int = 1,
    items_per_page: int = 5,
    sort_by: List[str] = None,
    descending: List[bool] = None,
    # current_user: DispatchUser = None,
    # role: UserRoles = UserRoles.member,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    model_cls = get_class_by_tablename(model)

    try:
        query = db_session.query(model_cls)

        if query_str:
            sort = False if sort_by else True
            query = search(query_str=query_str, query=query, model=model, sort=sort)

        # query_restricted = apply_model_specific_filters(model_cls, query, current_user, role)

        # tag_all_filters = []
        # if filter_spec:
        #     query = apply_filter_specific_joins(model_cls, filter_spec, query)
        #     # if the filter_spec has the TagAll filter, we need to split the query up
        #     # and intersect all of the results
        #     if has_tag_all(filter_spec):
        #         new_filter_spec, tag_all_spec = rebuild_filter_spec_without_tag_all(filter_spec)
        #         if new_filter_spec:
        #             query = apply_filters(query, new_filter_spec, model_cls)
        #         for tag_filter in tag_all_spec:
        #             tag_all_filters.append(apply_filters(query, tag_filter, model_cls))
        #     else:
        #         query = apply_filters(query, filter_spec, model_cls)

        # if model == "Incident":
        #     query = query.intersect(query_restricted)
        #     for filter in tag_all_filters:
        #         query = query.intersect(filter)

        # if model == "Case":
        #     query = query.intersect(query_restricted)
        #     for filter in tag_all_filters:
        #         query = query.intersect(filter)

        if sort_by:
            sort_spec = create_sort_spec(model, sort_by, descending)
            query = apply_sort(query, sort_spec)

    except FieldNotFound as e:
        raise ValidationError.from_exception_data(
            title=model_cls.__name__,
            line_errors=[InitErrorDetails(type=FieldNotFoundError(msg=str(e)), loc=("filter",))],
        ) from None
    except BadFilterFormat as e:
        raise ValidationError.from_exception_data(
            title=model_cls.__name__,
            line_errors=[InitErrorDetails(type=InvalidFilterError(msg=str(e)), loc=("filter",))],
        ) from None

    if items_per_page == -1:
        items_per_page = None

    # sometimes we get bad input for the search function
    # TODO investigate moving to a different way to parsing queries that won't through errors
    # e.g. websearch_to_tsquery
    # https://www.postgresql.org/docs/current/textsearch-controls.html
    try:
        query, pagination = apply_pagination(query, page_number=page, page_size=items_per_page)
    except ProgrammingError as e:
        logger.debug(e)
        return {
            "items": [],
            "itemsPerPage": items_per_page,
            "page": page,
            "total": 0,
        }

    return {
        "items": query.all(),
        "itemsPerPage": pagination.page_size,
        "page": pagination.page_number,
        "total": pagination.total_results,
    }
