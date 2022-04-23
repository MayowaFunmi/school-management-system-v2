from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import School, Zone


def get_school_by_zone(request):
    selected_zone_id = request.GET.get('selected_zone_id', None)
    selected_zone = Zone.objects.get(id=selected_zone_id)
    schools = School.objects.filter(zone=selected_zone)
    t = render_to_string('auths/school_by_zone.html', {'data': schools})
    return JsonResponse({'data': t})


'''class GetSchoolByZone(View):
    def get(self, request):
        selected_zone = request.GET.get('selected_zone', None)
        schools = School.objects.filter(zone__name=selected_zone)
        print(schools)'''