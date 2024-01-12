from rest_framework import generics
from ..models import Subject
from .serializers import SubjectSerializer, CourseSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    # include an id URl parameter for the detail view to retrieve the 'id' object
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# all the information about authentication at: https://www.djangorest-framework.org/api-guide/authentication/
class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # provide only read actions-list and retrieve
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get', 'post'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def enroll(self, request, *args, **kwargs):
    #     course = self.get_object()
    #     course.student.add(request.user)
    #     return Response({'enrolled': True})
