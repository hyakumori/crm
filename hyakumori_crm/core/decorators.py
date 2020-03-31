from functools import wraps
from datetime import datetime
import pytz
from pydantic import ValidationError


def validate_model(input_model, get_func=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(_, info, **kwargs) -> dict:
            try:
                data = kwargs["data"]
                pk = kwargs.get("pk")
                # when update obj
                if pk:
                    assert get_func is not None, "get_func can't be None"
                    obj = get_func(pk=pk)
                    if not obj:
                        return {"ok": False, "error": {"msg": "Not found"}}
                    del kwargs["pk"]
                    kwargs["obj"] = obj
                    data["context"] = {"updated_at": obj.updated_at}
                validated_data = input_model(**data).dict()
            except ValidationError as e:
                return {"ok": False, "error": e.errors()}
            kwargs["data"] = validated_data
            try:
                output = f(_, info, **kwargs)
            except Exception as e:
                return {"ok": False, "error": dict(message=str(e))}
            return {"ok": True, **output}

        return decorated_function

    return decorator
