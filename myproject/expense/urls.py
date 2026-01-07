from django.urls import path
from . import views
from .views import ExpenseAPI

urlpatterns = [
    #path('', ExpenseAPI.as_view(), name='root'),
    path('',views.ExpenseAPI.as_view(), name="expense_api"),      # GET, POST
    path('<int:id>/',ExpenseAPI.as_view(), name="expense_api" ),  # GET, PUT, DELETE
]


    

