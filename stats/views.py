from django.http import JsonResponse
from django.shortcuts import render
from auths.models import TeachingSTaff
from django.template.loader import render_to_string

from .utils import get_user_from_id, get_zone_from_id, get_school_from_id, get_subject_from_id
import pandas as pd
# Create your views here.


def home(request):
    fields = ['user_id', 'gender', 'date_of_birth', 'age', 'religion', 'created_date', 'designation', 'grade_level',
              'first_appointment', 'qualification', 'years_in_service', 'discipline', 'current_posting_zone_id',
              'current_posting_school_id', 'current_subject_id']
    staff_data = TeachingSTaff.objects.all().values()
    teachers_df = pd.DataFrame(staff_data, columns=fields)
    #zone1_teachers = teachers_df['current_posting_zone_id']
    zone1 = teachers_df[teachers_df['current_posting_zone_id'] == 'Zone 1']
    print('zone1 = ', zone1)
    teachers_df['user_id'] = teachers_df['user_id'].apply(get_user_from_id)
    teachers_df['current_posting_zone_id'] = teachers_df['current_posting_zone_id'].apply(get_zone_from_id)
    teachers_df['current_posting_school_id'] = teachers_df['current_posting_school_id'].apply(get_school_from_id)
    teachers_df['current_subject_id'] = teachers_df['current_subject_id'].apply(get_subject_from_id)
    teachers_df['created_date'] = teachers_df['created_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    teachers_df.rename({'user_id': 'name', 'created_date': 'date_registered', 'first_appointment': 'first appointment',
                        'years_in_service': 'Years In Service', 'current_posting_zone_id': 'Zone',
                        'current_posting_school_id': 'School', 'current_subject_id': 'Subject'}, axis=1, inplace=True)
    #teachers_df.drop(['])  drop columns
    # filter for a value in column values e.g get all zone 1 details

    context = {
        'teachers_df': teachers_df.to_html,
        'zone1': zone1.to_html
    }
    if request.method == 'POST':
        form = request.POST.getlist('column_1')
        #print(form)

    return render(request, 'stats/home.html', context)


def get_table_data(request):
    fields = request.GET.get('fields', None)
    staff_data = TeachingSTaff.objects.all().values()
    teachers_df = pd.DataFrame(staff_data, columns=fields)
    teachers_df['user_id'] = teachers_df['user_id'].apply(get_user_from_id)
    teachers_df['current_posting_zone_id'] = teachers_df['current_posting_zone_id'].apply(get_zone_from_id)
    teachers_df['current_posting_school_id'] = teachers_df['current_posting_school_id'].apply(get_school_from_id)
    teachers_df['current_subject_id'] = teachers_df['current_subject_id'].apply(get_subject_from_id)
    teachers_df['created_date'] = teachers_df['created_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    teachers_df.rename({'user_id': 'name', 'created_date': 'date_registered', 'first_appointment': 'first appointment',
                        'years_in_service': 'Years In Service', 'current_posting_zone_id': 'Zone',
                        'current_posting_school_id': 'School', 'current_subject_id': 'Subject'}, axis=1, inplace=True)
    teacher_html = teachers_df
    print(teacher_html)
    t = render_to_string('stats/teacher_table.html', {'data': teacher_html})
    return JsonResponse({'data': t})

'''
entries = my_model.objects.all()   

# this generates an array containing the names of the model fields
columns_names = [field.name for field in my_model._meta.get_fields()]

L_GI = len(entries)

    # generate empty dataframe
    GI = pd.DataFrame(columns = columns_names)

    for element in entries:       
        new_entry = {"Field_A":element.Field_A, "Field_B":element.Field_B, "Field_C":element.Field_C}
        GI = GI.append(new_entry, ignore_index=True)
'''