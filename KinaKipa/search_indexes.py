from datetime import datetime
from haystack import indexes
from KinaKipa.models import Article, Film

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='published_date')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published_date__lte=datetime.now())


class FilmIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    name_origin = indexes.CharField(model_attr='name_origin')
    year = indexes.CharField(model_attr='year')

    def get_model(self):
        return Film

    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('name')
