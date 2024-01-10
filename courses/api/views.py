from rest_framework import generics
from ..models import Subject
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    # include an id URl parameter for the detail view to retrieve the 'id' object
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
