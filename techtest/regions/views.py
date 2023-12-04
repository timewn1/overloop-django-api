import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.regions.models import Region
from techtest.regions.schemas import RegionSchema
from techtest.utils import json_response


class RegionsListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(RegionSchema().dump(Region.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            region = RegionSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(RegionSchema().dump(region), 201)


class RegionView(View):
    def dispatch(self, request, region_id, *args, **kwargs):
        try:
            self.region = Region.objects.get(pk=region_id)
        except Region.DoesNotExist:
            return json_response({"error": "No Region matches the given query"}, 404)
        self.data = request.body and dict(json.loads(request.body), id=self.region.id)
        return super(RegionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return json_response(RegionSchema().dump(self.region))

    def put(self, request, *args, **kwargs):
        try:
            self.region = RegionSchema().load(self.data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(RegionSchema().dump(self.region))

    def delete(self, request, *args, **kwargs):
        self.region.delete()
        return json_response()
