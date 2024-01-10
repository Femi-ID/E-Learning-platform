from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView


class StudentRegistrationView(CreateView):
    """View to allow students to register."""
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm  # registration modelform to create user objects
    success_url = reverse_lazy('student_course_list')  # URL to redirect user upon successful submission

    def form_valid(self, form):
        """Executed when valid form data has been posted."""
        result = super().form_valid(form)
        cd = form.cleaned_data
        # You override this method to login the user after successfully signing up
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """To enroll a student to a course, no view needed."""
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """Executed when the form is valid and adds the current user to the students enrolled on the course."""
        self.course = form.cleaned_data['course']  # To store the given course object
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):  # equivalent to success_url attribute
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """View for the logged-in user(student) to see the courses they've enrolled for."""
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])  # to get all courses and filter the courses enrolled by the user


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # limit query to courses enrolled by the user
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()

        if 'module_id' in self.kwargs:
            # get current module to include a module in the context if module_id is given
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # Otherwise get first module of the course
            context['module'] = course.modules.all()[0]
            # context['module'] = course.modules.first()
        return context

# Clear db, delete sqlite and migrate again

