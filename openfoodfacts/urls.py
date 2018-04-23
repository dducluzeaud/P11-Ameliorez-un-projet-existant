from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('product_search/', views.ProductsListView.as_view(), name='products_list'),
    path('<int:id_product>/', views.detail, name='detail'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('register/', views.sign_up, name='sign_up'),
    path('account/', views.account, name='account'),
    path('contacts/', views.contacts, name='contacts'),
    path('legals/', views.legals, name='legals'),
    path('saved/', views.saved, name='saved'),
    path('', include('django.contrib.auth.urls'))

]
