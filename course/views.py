from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from studentHelper.models import Course
from studentHelper.views import main_view


@login_required(login_url='/login')
def course_view(request, pk):
    context = {
        'course': Course.objects.get_record_by_id(pk)
    }

    if context['course'].client_id != request.user:
        return main_view(request)

    return render(request, "course.html", context)


@login_required(login_url='/login')
def temp(request):
    pass
