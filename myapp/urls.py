from django.urls import path
from . import views

urlpatterns = [
    path('api/create-user/', views.create_user),
    path('api/user-details/<int:user_id>/', views.get_user_details),
    path('api/add-expense/', views.add_expense, name='add_expense'),
    path('api/user-expenses/<int:user_id>/', views.user_expenses, name='user_expenses'),
    path('api/overall-expenses/', views.overall_expenses, name='overall_expenses'),
    path('api/download-balance-sheet/', views.download_balance_sheet, name='download_balance_sheet'),
]
