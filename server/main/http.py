from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse as _JsonResponse
from ulid.ulid import ULID


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ULID):
            return str(obj)
        return super().default(obj)


def JsonResponse(*args, **kwargs):
    kwargs["encoder"] = CustomJsonEncoder
    return _JsonResponse(*args, **kwargs)
