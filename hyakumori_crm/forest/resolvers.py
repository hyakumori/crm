from ariadne import QueryType

from ..core.decorators import validate_model
from ..core.models import Paginator
from .service import get_forests_by_condition

query = QueryType()

@query.field("list_forests")
@validate_model(Paginator)
def get_list_forests(_, info, data) -> dict:
    return get_forests_by_condition(data)

resolvers = [query]
