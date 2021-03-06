from loans.models import Loan, LoanPayment
from codenation.utils.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(max_digits=18, decimal_places=6)
    term = serializers.IntegerField(source='amount_of_payments')
    rate = serializers.DecimalField(max_digits=4, decimal_places=3, source='interest_rate')
    date = serializers.DateTimeField(source='requested_date')
    client_id = serializers.UUIDField(source='client')
    
    class Meta:
        model = Loan
        fields = ('client_id', 'amount', 'term', 'rate', 'date',)


class LoanPaymentSerializer(serializers.ModelSerializer):

    payment = serializers.CharField(source='payment_type')
    date = serializers.DateTimeField(source='payment_date')
    amount = serializers.DecimalField(max_digits=18, decimal_places=6, source='payment_amount')

    class Meta:
        model = LoanPayment
        fields = ('payment', 'date', 'amount',)


class LoanPaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'


class LoanDetailSerializer(LoanSerializer, DynamicFieldsModelSerializer):

    loan_id = serializers.UUIDField()
    payments = LoanPaymentDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Loan
        fields = ('loan_id', 'payment_amount',) + LoanSerializer.Meta.fields + ('payments',)


class LoanPaymentBalanceSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
