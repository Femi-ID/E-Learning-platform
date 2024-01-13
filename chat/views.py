from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.response import Response
from rest_framework import status


@login_required
def course_chat_room(request, course_id):
    try:
        # retrieve course with given id enrolled by the current user
        course = request.user.courses_joined.get(id=course_id)
        if not course:
            return Response({'status': 404, 'success': False,
                             'message': 'Course object not found'},
                            status=status.HTTP_404_NOT_FOUND)
    except Exception:
        # user is not an enrolled student of the course or course doesn't exist
        return Response({'status': 403, 'success': False,
                         'message': 'User is not an enrolled student for the course'},
                        status=status.HTTP_403_FORBIDDEN)
    return render(request, 'chat/room.html', {'course': course})



