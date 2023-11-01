from django.shortcuts import render
from .models import Course
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
"""
Mixins are a special kind of multiple inheritance for a class. You can use them
to provide common discrete functionality that, when added to other mixins, allows
you to define the behavior of a class.
"""
# class ManageCourseListView(ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(owner=self.request.user)


class OwnerMixin(object):
    """Returns a queryset of objects belonging to the current user.
    Can be used for any views that interact with any model that containing owner attribute"""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """To assign the form to the current logged-in user."""
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """OwnerMixin class can be used for views that interact with any model that contains an owner attribute"""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """used by views with forms or model forms such as CreateView and UpdateView. form_valid()"""
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    # Uses a model form to create a new Course object.
    # It uses the fields defined in OwnerCourseMixin to build a model form
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    # Allows the editing of an existing Course object.
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
