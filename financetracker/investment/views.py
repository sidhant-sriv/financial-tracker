from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Portfolio, Investment
from .serializers import PortfolioSerializer, InvestmentSerializer

class PortfolioListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            portfolios = Portfolio.objects.filter(user=request.user)
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = PortfolioSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortfolioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Portfolio.objects.get(pk=pk, user=user)
        except Portfolio.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        portfolio = self.get_object(pk, request.user)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        portfolio = self.get_object(pk, request.user)
        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        portfolio = self.get_object(pk, request.user)
        try:
            portfolio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InvestmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, portfolio_pk):
        try:
            investments = Investment.objects.filter(portfolio__pk=portfolio_pk, portfolio__user=request.user)
            serializer = InvestmentSerializer(investments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, portfolio_pk):
        try:
            portfolio = Portfolio.objects.get(pk=portfolio_pk, user=request.user)
            data = request.data
            data['portfolio'] = portfolio.id
            if portfolio.remaining_budget < float(data['amount']):
                return Response({"error": "Insufficient budget."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = InvestmentSerializer(data=data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvestmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Investment.objects.get(pk=pk, portfolio__user=user)
        except Investment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        investment = self.get_object(pk, request.user)
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        investment = self.get_object(pk, request.user)
        serializer = InvestmentSerializer(investment, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        investment = self.get_object(pk, request.user)
        try:
            investment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
