from ariadne import QueryType

from .service import get_forests_by_condition

query = QueryType()

@query.field("list_forests")
def get_list_forests(_, info, filter) -> dict:
    return get_forests_by_condition(filter)

resolvers = [query]
