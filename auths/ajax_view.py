from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import School, Zone, Student


def get_school_by_zone(request):
    selected_zone_id = request.GET.get('selected_zone_id', None)
    selected_zone = Zone.objects.get(id=selected_zone_id)
    schools = School.objects.filter(zone=selected_zone)
    t = render_to_string('auths/school_by_zone.html', {'data': schools})
    return JsonResponse({'data': t})


def get_student_by_school(request):
    selected_school_id = request.GET.get('selected_school_id', None)
    selected_school = School.objects.get(id=selected_school_id)
    all_students = Student.objects.filter(current_school=selected_school)
    paginator = Paginator(all_students, 4)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    t = render_to_string('auths/students_by_school.html', {'data': students})
    return JsonResponse({'data': t})