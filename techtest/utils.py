import json
from django.http.response import HttpResponse


def json_response(data={}, status=200):
    return HttpResponse(
        content=json.dumps(data), status=status, content_type="application/json"
    )
