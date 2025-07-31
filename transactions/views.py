from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-date')

        tx_type = self.request.query_params.get('type')
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')
        min_value = self.request.query_params.get('min_value')
        max_value = self.request.query_params.get('max_value')

        if tx_type:
            queryset = queryset.filter(type=tx_type)
        if date_after:
            queryset = queryset.filter(date__gte=date_after)
        if date_before:
            queryset = queryset.filter(date__lte=date_before)
        if min_value:
            queryset = queryset.filter(value__gte=min_value)
        if max_value:
            queryset = queryset.filter(value__lte=max_value)

        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class BalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        saldo = 0
        for t in transactions:
            if t.type == 'entrada':
                saldo += t.value
            else:
                saldo -= t.value
        return Response({'balance': saldo})
