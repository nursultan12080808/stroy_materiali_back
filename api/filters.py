import django_filters

from stroy.models import *

class MaterialFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    class Meta:
        model = Material
        fields = ['category','company','currency', 'price_for','tags']