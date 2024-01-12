from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def course_chat_room(request, course_id):
    try:
        # retrieve course with given id enrolled by the current user
        course = request.user.courses_joined.get(id=course_id)
        if not course:
            return
    except:
        # user is not a student of the course or course doesn't exist
        return HttpResponseForbidden()



