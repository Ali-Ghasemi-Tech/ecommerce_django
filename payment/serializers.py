from rest_framework import serializers

class PaymentInitiateSerializer(serializers.Serializer):
    amount = serializers.IntegerField()  # In Rials
    order_id = serializers.IntegerField()
