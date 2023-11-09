from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
#  HiddenInput: to hide the field, a button will be displayed to enroll users


