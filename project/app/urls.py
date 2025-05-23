from django.urls import path
from . import views

app_name='app'

urlpatterns = [
    path('', views.home, name='home'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/download/', views.download_sales_excel, name='download_sales_excel'), 
    path('addsale/', views.add_sale, name='addsale'),

    # Dynamic route should be last
    path('<str:customer_id>/', views.customer_detail, name='customer_detail'),
]
