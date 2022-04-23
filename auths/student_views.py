from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Student, StudentFiles, School, Class, Level, Department


@login_required
def create_student_profile(request):
    all_schools = School.objects.order_by('name')
    all_departments = Department.objects.order_by('department')
    all_classes = Class.objects.order_by('name')
    all_levels = Level.objects.order_by('level')

    if request.method == 'POST':
        middle_name = request.POST['middle_name']
        admission_year = request.POST['admission_year']
        current_school_id = request.POST['current_school']
        department_id = request.POST['department']
        std_class_id = request.POST['std_class']
        level_id = request.POST['level']
        prev_school_1_id = request.POST['prev_school_1']
        prev_school_2_id = request.POST['prev_school_2']
        prev_school_3_id = request.POST['prev_school_3']
        picture = request.FILES['picture']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        age = request.POST['age']
        address = request.POST['address']
        religion = request.POST['religion']
        student_phone_number = request.POST['student_phone_number']
        father_name = request.POST['father_name']
        father_phone = request.POST['father_phone']
        mother_name = request.POST['mother_name']
        mother_phone = request.POST['mother_phone']
        father_img = request.FILES['father_img']
        mother_img = request.FILES['mother_img']

        if prev_school_1_id == 'Not Available':
            prev_school_1 = None
        else:
            prev_school_1 = School.objects.get(id=prev_school_1_id)

        if prev_school_2_id == 'Not Available':
            prev_school_2 = None
        else:
            prev_school_2 = School.objects.get(id=prev_school_2_id)

        if prev_school_3_id == 'Not Available':
            prev_school_3 = None
        else:
            prev_school_3 = School.objects.get(id=prev_school_3_id)

        current_school = School.objects.get(id=current_school_id)
        department = Department.objects.get(id=department_id)
        std_class = Class.objects.get(id=std_class_id)
        level = Level.objects.get(id=level_id)

        student = Student.objects.get(user=request.user)
        student.middle_name = middle_name
        student.admission_year = admission_year
        student.current_school = current_school
        student.department = department
        student.std_class = std_class
        student.level = level
        student.prev_school_1 = prev_school_1
        student.prev_school_2 = prev_school_2
        student.prev_school_3 = prev_school_3
        student.picture = picture
        student.gender = gender
        student.date_of_birth = date_of_birth
        student.age = age
        student.address = address
        student.religion = religion
        student.student_phone_number = student_phone_number
        student.father_name = father_name
        student.father_phone = father_phone
        student.mother_name = mother_name
        student.mother_phone = mother_phone
        student.father_img = father_img
        student.mother_img = mother_img
        student.save()

        # add files for students
        try:
            if request.FILES.getlist('documents'):
                images = request.FILES.getlist('documents')
                document_title = request.POST.getlist('document_title[]')
                print(document_title, type(document_title))
                file_list = []
                for image in images:
                    fs = FileSystemStorage()
                    file_path = fs.save(image.name, image)
                    file_list.append(file_path)

                print(file_list, type(file_list))
                for key, value in zip(document_title, file_list):
                    student_files = StudentFiles(user=student, document_title=key, documents=value)
                    student_files.save()
        except:
            pass

        return redirect('/auths/display_student_profile/')

    context = {
        'all_schools': all_schools,
        'all_departments': all_departments,
        'all_classes': all_classes,
        'all_levels': all_levels,
    }
    return render(request, 'auths/create_student_profile.html', context)


@login_required
def display_student_profile(request):
    student = Student.objects.get(user=request.user)
    student_file = StudentFiles.objects.filter(user=student)

    if student.middle_name is None:
        messages.info(request, 'You have no profile yet. Please create your profile.')
        return HttpResponseRedirect('/auths/create_student_profile/')
    else:
        context = {
            'username': request.user.username, 'first_name': request.user.first_name,
            'last_name': request.user.last_name, 'email': request.user.email, 'status': request.user.status,
            'admission_number': request.user.file_no, 'unique_id': request.user.unique_id, 'middle_name': student.middle_name,
            'admission_year': student.admission_year, 'current_school': student.current_school, 'department': student.department,
            'std_class': student.std_class, 'level': student.level, 'prev_school_1': student.prev_school_1,
            'prev_school_2': student.prev_school_2, 'prev_school_3': student.prev_school_3, 'picture': student.picture,
            'gender': student.gender, 'date_of_birth': student.date_of_birth, 'age': student.age, 'address': student.address,
            'religion': student.religion, 'student_phone_number': student.student_phone_number, 'father_name': student.father_name,
            'father_phone': student.father_phone, 'father_img': student.father_img, 'mother_name': student.mother_name,
            'mother_phone': student.mother_phone, 'mother_img': student.mother_img, 'created_date': student.created_date,
        }
        return render(request, 'auths/display_student_profile.html', context)


@login_required
def update_student_profile(request):
    student = Student.objects.get(user=request.user)
    all_schools = School.objects.order_by('name')
    all_departments = Department.objects.order_by('department')
    all_classes = Class.objects.order_by('name')
    all_levels = Level.objects.order_by('level')
    context = {
        'student': student,
        'all_schools': all_schools,
        'all_departments': all_departments,
        'all_classes': all_classes,
        'all_levels': all_levels,
    }
    return render(request, 'auths/update_student_profile.html', context)