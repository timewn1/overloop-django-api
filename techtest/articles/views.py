import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.articles.models import Article
from techtest.articles.schemas import ArticleSchema
from techtest.utils import json_response


class ArticlesListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(ArticleSchema().dump(Article.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            article = ArticleSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(article), 201)


class ArticleView(View):
    def dispatch(self, request, article_id, *args, **kwargs):
        try:
            self.article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return json_response({"error": "No Article matches the given query"}, 404)
        self.data = request.body and dict(json.loads(request.body), id=self.article.id)
        return super(ArticleView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return json_response(ArticleSchema().dump(self.article))

    def put(self, request, *args, **kwargs):
        try:
            self.article = ArticleSchema().load(self.data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(self.article))

    def delete(self, request, *args, **kwargs):
        self.article.delete()
        return json_response()
