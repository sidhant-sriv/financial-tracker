from rest_framework import serializers
from .models import Investment, Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
        class Meta:
            model = Portfolio
            fields = '__all__'

class InvestmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Investment
            fields = '__all__'