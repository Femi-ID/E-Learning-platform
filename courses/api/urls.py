from django.urls import path, include
from rest_framework import routers
from . import views

# app_name = 'courses'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
# to register the viewset with the 'courses' prefix

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
#     path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
#     path('courses/<int:pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),
# ]
