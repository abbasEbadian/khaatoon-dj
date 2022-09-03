from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Khaatoon' )

urlpatterns = [
    path('category/', include('category.urls')),
    path('product/', include('product.urls')),
    path('users/', include('users.urls')),
    path('favorite/', include('favorite.urls')),
    path('reminder/', include('reminder.urls')),
    path('state/', include('state.urls')),
    path('market/', include('market.urls')),
    path('address/', include('address.urls')),
    path('message/', include('message.urls')),
    path('attribute/', include('attribute.urls')),
    path('ticket/', include('ticket.urls')),
    path('order/', include('order.urls')),
    path('config/', include('config.urls')),
    path('swagger/', schema_view)
]