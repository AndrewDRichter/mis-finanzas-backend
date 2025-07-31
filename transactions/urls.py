from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyView, BalanceView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('balance/', BalanceView.as_view(), name='balance'),
    path('<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
