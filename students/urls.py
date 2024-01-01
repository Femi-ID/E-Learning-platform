from django.urls import path
from . import views
from django.views.decorators.cache import cache_page  # to cache the output of individual views.


urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<int:pk>/', cache_page(60 * 15)(views.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<int:pk>/module/<int:module_id>', cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
         name='student_course_detail_module'),

]


# The per-view cache uses the URL to build the cache key. Multiple
# URLs pointing to the same view will be cached separately.
