from ariadne import ObjectType
from pydantic import ValidationError

from .models import ClientCreate, Client, ClientRead

query = ObjectType("Query")
mutation = ObjectType("Mutation")


@query.field("get_client")
def get_client_by_id(*_, id: str = None) -> dict:
    return {
        "ok": True,
        "client": {
            "id": "asdaqw1273ajshdkc",
            "internal_id": "ajshdq8w123",
            "profile": {"first_name": "Ha", "last_name": "Tran", "middle_name": None},
            "attributes": None,
        },
    }


@mutation.field("create_client")
def create_client(*_, data: dict = None) -> dict:
    try:
        c = Client(**ClientCreate(**data).dict())
        c.save()
        return {"ok": True, "client": ClientRead.from_orm(c).dict()}
    except ValidationError as e:
        return {"ok": False, "error": e.errors()}


resolvers = [query, mutation]
