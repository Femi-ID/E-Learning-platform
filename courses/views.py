from .models import Course
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormset
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Content, Module
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm
from django.core.cache import cache
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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """This view handles the formset to add, update and delete modules for a specific course."""
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, pk):
        # It's provided by the View class. It takes an HTTP request and its parameters
        # and attempts to delegate to a lowercase method that matches the HTTP method used.
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """To create and update different models' contents."""
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        # model_name-name of the content(video, image, text...) to be created/updated
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order',
                                                 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """It receives the URL parameters and stores them as class attributes."""
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        # You build the model form for the Text, Video, Image, or File instance that is being updated.
        # Or you pass no instance to create a new object, since self.obj=None if id=None
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # id(for video, text...) doesn't exist, then create a new content
                Content.objects.create(module=self.module, item=obj)
                return redirect('module_content_list', self.module.id)
            return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View, TemplateResponseMixin):
    """views to delete course modules' contents"""

    def post(self, request, id):
        try:
            content = get_object_or_404(Content, id=id, module__course__owner=request.user)
            module = content.module
            # To delete the related Text, Video, Image, or File object and then delete the Content object
            content.item.delete()
            content.delete()
        except Content.DoesNotExist:
            return self.render_to_response({'error': "Content not found, doesn't exist",
                                            'success': True,
                                            'status_code': 404
                                            })
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """List the contents of a specific module"""
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        # gets the Module object with the given ID that belongs to the current user
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """To provide a simple way to reorder course's modules"""

    def post(self, request):
        # To re-order every module for that particular course
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """To provide a simple way to reorder modules' contents."""

    def post(self, request):
        # To re-order every content for that particular content
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    """Display all available courses for students to browse and enroll on them."""
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        # You retrieve all subjects, using the ORM's annotate() method with the Count() aggregation function
        # to include the total number of courses for each subject. Same with modules for courses.
        subjects = cache.get('all_subjects')
        if not subjects:  # if it hasn't been cached yet or timed out, you set it
            # cache.set(key, value, timeout)
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)

        all_courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            # If given, retrieve the corresponding subject object
            subject = get_object_or_404(Subject, slug=subject)
            # you'll want to cache something that is based on dynamic data. In these cases, you have to
            # build dynamic keys that contain all the information required to uniquely identify the cached data.
            key = f'subject_{subject.id}_courses'  # caching based on dynamic data
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)  # limit the query by the courses belonging to the subject
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)  # to set an "all_courses" key to all_courses
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DetailView):
    """Display a single course overview"""
    model = Course
    template_name = 'courses/course/detail.html'
    # Django's DetailView expects a primary key (pk) or slug URL parameter to retrieve
    # a single object for the given model. To be sent in the view template.

    # To include the enrollment form in the context for rendering templates.
    # You initialize the hidden course field of the form with the current Course object
    # so that it can be submitted directly
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


