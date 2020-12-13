from studentHelper.models import Course


def courses_context(request):
    courses = Course.objects.get_main_records_by_client_id(request.user.id)
    return {'courses': courses}
