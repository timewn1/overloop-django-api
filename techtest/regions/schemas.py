from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from techtest.regions.models import Region


class RegionSchema(Schema):
    class Meta(object):
        model = Region

    id = fields.Integer()
    code = fields.String(required=True, validate=validate.Length(equal=2))
    name = fields.String(validate=validate.Length(max=255))

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        region, _ = Region.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        return region
