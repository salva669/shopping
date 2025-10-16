from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class BidhaaViewSet(viewsets.ModelViewSet):
    queryset = Bidhaas.objects.all()
    serializer_class = BidhaaSerializer
    
    @action(detail=False, methods=['get'])
    def sync(self, request):
        """Get all items modified after a timestamp"""
        last_sync = request.query_params.get('last_sync')
        if last_sync:
            queryset = self.queryset.filter(updated_at__gt=last_sync)
        else:
            queryset = self.queryset.all()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'timestamp': timezone.now().isoformat()
        })

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple sales from offline queue"""
        sales_data = request.data.get('sales', [])
        created_sales = []
        
        for sale_data in sales_data:
            serializer = self.get_serializer(data=sale_data)
            if serializer.is_valid():
                sale = serializer.save()
                created_sales.append(sale)
        
        return Response({
            'created': len(created_sales),
            'sales': SaleSerializer(created_sales, many=True).data
        })

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer