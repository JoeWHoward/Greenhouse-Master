from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import TempHumRecordSerializer
from .models import TempHumRecord

# Create your views here.
class TempHumRecordCreateView(CreateAPIView):
    queryset = TempHumRecord.objects.all()
    serializer_class = TempHumRecordSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}