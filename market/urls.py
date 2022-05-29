from django.urls import path, include
from . import views
urlpatterns = [
    # path('market/<int:pk>/', views.get_market_data),
    # path('market/business/all/', views.get_all_businesses),
    path('business_and_province/all/', views.get_all_business_and_province),
    path('image/cover/', views.upload_cover_image),
    path('image/avatar/', views.upload_avatar_image),
    path('update/', views.update_market_detail),
    path('update_bank/', views.update_market_detail_bank),
    path('update_document/', views.update_market_document),
    path('bank/all/', views.get_all_banks),
    path('<str:username>/', views.get_market_by_user_name),

]