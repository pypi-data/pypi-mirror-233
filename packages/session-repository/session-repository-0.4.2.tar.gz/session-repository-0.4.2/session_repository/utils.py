# MODULES
from dataclasses import dataclass
import json
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

# SQLALCHEMY
from sqlalchemy import and_, asc, desc, tuple_, func
from sqlalchemy.orm import (
    Query,
    InstrumentedAttribute,
    noload,
    lazyload,
    joinedload,
    subqueryload,
    selectinload,
    raiseload,
)
from sqlalchemy.sql.elements import Null

# Enum
from session_repository.enum import LoadingTechnique, Operators

_FilterType = Dict[Union[InstrumentedAttribute, Tuple[InstrumentedAttribute]], Any]


@dataclass
class RelationshipOption:
    lazy: LoadingTechnique
    childs: Optional[Dict[InstrumentedAttribute, "RelationshipOption"]] = None


def apply_relationship_options(
    query: Query,
    relationship_options: Dict[InstrumentedAttribute, RelationshipOption],
    parents: List[InstrumentedAttribute] = None,
):
    if relationship_options is None:
        return query

    for relationship, sub_relationships in relationship_options.items():
        if relationship is None or not isinstance(relationship, InstrumentedAttribute):
            continue
        if sub_relationships is None or not isinstance(
            sub_relationships, RelationshipOption
        ):
            continue

        sub_items = [relationship] if parents is None else [*parents, relationship]
        match sub_relationships.lazy:
            case LoadingTechnique.LAZY:
                query = query.options(lazyload(*sub_items))
            case LoadingTechnique.JOINED:
                query = query.options(joinedload(*sub_items))
            case LoadingTechnique.SUBQUERY:
                query = query.options(subqueryload(*sub_items))
            case LoadingTechnique.SELECTIN:
                query = query.options(selectinload(*sub_items))
            case LoadingTechnique.RAISE:
                query = query.options(raiseload(*sub_items))
            case LoadingTechnique.NOLOAD:
                query = query.options(noload(*sub_items))

        if sub_relationships.childs is not None:
            query = apply_relationship_options(
                query,
                relationship_options=sub_relationships.childs,
                parents=sub_items,
            )

    return query


def apply_no_load(
    query: Query,
    relationship_dict: Dict[InstrumentedAttribute, Any],
    parents: List[InstrumentedAttribute] = None,
):
    if relationship_dict is None:
        return query

    for relationship, sub_relationships in relationship_dict.items():
        if relationship is None or not isinstance(relationship, InstrumentedAttribute):
            continue

        sub_items = [relationship] if parents is None else [*parents, relationship]
        if sub_relationships is None:
            query = query.options(noload(*sub_items))
        else:
            query = apply_no_load(
                query,
                relationship_dict=sub_relationships,
                parents=sub_items,
            )

    return query


def apply_filters(
    query: Query,
    filter_dict: _FilterType,
    with_optional: bool = False,
):
    filters = get_filters(
        filters=filter_dict,
        with_optional=with_optional,
    )

    return query if len(filters) == 0 else query.filter(and_(*filters))


def apply_order_by(
    query: Query,
    model,
    order_by: Union[List[str], str],
    direction: Union[List[str], str],
):
    if order_by is None or direction is None:
        return query

    if isinstance(order_by, str):
        order_by = [order_by]

    if isinstance(direction, str):
        direction = [direction]

    if len(order_by) != len(direction):
        raise ValueError("order_by length must be equals to direction length")

    order_by_list = []
    for column, dir in zip(order_by, direction):
        if dir == "desc":
            order_by_list.append(desc(getattr(model, column)))
        elif dir == "asc":
            order_by_list.append(asc(getattr(model, column)))

    return query.order_by(*order_by_list)


def build_order_by(
    model,
    order_by: dict,
):
    if isinstance(order_by, dict):
        order_by_list = []
        for key, value in order_by.items():
            if isinstance(value, dict):
                relationship = getattr(model, key)
                order_by_relationship = build_order_by(value, relationship)
                order_by_list.extend(order_by_relationship)
            else:
                column = getattr(model, key)
                if value == "ASC":
                    order_by_list.append(asc(column))
                elif value == "DESC":
                    order_by_list.append(desc(column))
        return order_by_list
    else:
        raise ValueError("Invalid nomenclature format.")


def apply_pagination(
    query: Query,
    page: int,
    per_page: int,
):
    pagination = None
    if page is not None and per_page is not None:
        total_results = query.count()
        total_pages = (total_results + per_page - 1) // per_page

        pagination = {
            "total": total_results,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
        }

        pagination = json.dumps(pagination)

        query = query.offset((page - 1) * per_page).limit(per_page)

    return query, pagination


def apply_limit(
    query: Query,
    limit: int,
):
    return query.limit(limit) if limit is not None else query


def get_conditions_from_dict(
    values: _FilterType,
    with_optional: bool = False,
):
    conditions = []
    for key, value in values.items():
        if type(value) == set:
            value = list(value)
        elif type(value) == dict:
            for k, v in value.items():
                if with_optional and v is None:
                    continue

                match k:
                    case Operators.EQUAL:
                        conditions.append(key == v)
                    case Operators.IEQUAL:
                        if not isinstance(v, Null):
                            conditions.append(func.lower(key) == func.lower(v))
                        else:
                            conditions.append(key == v)
                    case Operators.DIFFERENT:
                        conditions.append(key != v)
                    case Operators.IDIFFERENT:
                        if not isinstance(v, Null):
                            conditions.append(func.lower(key) != func.lower(v))
                        else:
                            conditions.append(key != v)
                    case Operators.LIKE:
                        if not isinstance(v, Null):
                            conditions.append(key.like(v))
                        else:
                            conditions.append(key == v)
                    case Operators.NOT_LIKE:
                        if not isinstance(v, Null):
                            conditions.append(~key.like(v))
                        else:
                            conditions.append(key != v)
                    case Operators.ILIKE:
                        if not isinstance(v, Null):
                            conditions.append(key.ilike(v))
                        else:
                            conditions.append(key == v)
                    case Operators.NOT_ILIKE:
                        if not isinstance(v, Null):
                            conditions.append(~key.ilike(v))
                        else:
                            conditions.append(key != v)
                    case Operators.BETWEEN:
                        if len(v) != 2:
                            continue
                        if v[0] is not None:
                            conditions.append(key > v[0])
                        if v[1] is not None:
                            conditions.append(key < v[1])
                    case Operators.BETWEEN_OR_EQUAL:
                        if len(v) != 2:
                            continue
                        if v[0] is not None:
                            conditions.append(key >= v[0])
                        if v[1] is not None:
                            conditions.append(key <= v[1])
                    case Operators.SUPERIOR:
                        conditions.append(key > v)
                    case Operators.INFERIOR:
                        conditions.append(key < v)
                    case Operators.SUPERIOR_OR_EQUAL:
                        conditions.append(key >= v)
                    case Operators.INFERIOR_OR_EQUAL:
                        conditions.append(key <= v)
                    case Operators.IN:
                        v = v if isinstance(v, Iterable) else [v]
                        if isinstance(key, tuple):
                            conditions.append(tuple_(*key).in_(v))
                        else:
                            conditions.append(key.in_(v))
                    case Operators.IIN:
                        v = v if isinstance(v, Iterable) else [v]
                        if isinstance(key, tuple):
                            conditions.append(
                                tuple_([func.lower(key_) for key_ in key]).in_(
                                    [
                                        func.lower(v_)
                                        if not isinstance(v_, Null)
                                        else v_
                                        for v_ in v
                                    ]
                                )
                            )
                        else:
                            conditions.append(
                                func.lower(key).in_(
                                    [
                                        func.lower(v_)
                                        if not isinstance(v_, Null)
                                        else v_
                                        for v_ in v
                                    ]
                                )
                            )
                    case Operators.NOT_IN:
                        v = v if isinstance(v, Iterable) else [v]
                        if isinstance(key, tuple):
                            conditions.append(tuple_(*key).notin_(v))
                        else:
                            conditions.append(key.notin_(v))

                    case Operators.NOT_IIN:
                        v = v if isinstance(v, Iterable) else [v]
                        if isinstance(key, tuple):
                            conditions.append(
                                tuple_([func.lower(key_) for key_ in key]).notin_(
                                    [
                                        func.lower(v_)
                                        if not isinstance(v_, Null)
                                        else v_
                                        for v_ in v
                                    ]
                                )
                            )
                        else:
                            conditions.append(
                                func.lower(key).notin_(
                                    [
                                        func.lower(v_)
                                        if not isinstance(v_, Null)
                                        else v_
                                        for v_ in v
                                    ]
                                )
                            )
                    case Operators.HAS:
                        v = get_filters(
                            v,
                            with_optional=with_optional,
                        )
                        for condition in v:
                            conditions.append(key.has(condition))
                    case Operators.ANY:
                        v = get_filters(
                            v,
                            with_optional=with_optional,
                        )

                        if len(v) == 0:
                            continue

                        conditions.append(key.any(and_(*v)))

    return conditions


def get_filters(
    filters: _FilterType,
    with_optional: bool = False,
):
    if filters is None:
        return []
    if not isinstance(filters, dict):
        raise TypeError("<filters> must be type of <dict>")

    filters = [{x: y} for x, y in filters.items()]

    conditions = []
    for filter_c in filters:
        if not type(filter_c) == dict:
            continue

        conditions_from_dict = get_conditions_from_dict(
            filter_c,
            with_optional=with_optional,
        )
        conditions.extend(conditions_from_dict)

    return conditions
