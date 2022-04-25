from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from .models import Zone, School, TeachingSTaff, TeachingSTaffFiles, Subject, Student, StudentFiles

# Create your views here.

User = get_user_model()


def home(request):
    return render(request, 'auths/login.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        file_no = request.POST['file_no']
        status = request.POST['status']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validate username
        check_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root', 'email',
                       'user', 'join', 'sql', 'static', 'python', 'delete', 'sex', 'sexy']

        if username in check_users:
            messages.error(request, 'Your Username, ' + username + ', Is Not Acceptable. Please Use Another Username')
            return render(request, 'auths/user_signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your Username, ' + username + ', Already Exists. Please Try Another Username')
            return render(request, 'auths/user_signup.html')

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'auths/user_signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ', Already Exists. Please Try Another Email')
            return render(request, 'auths/user_signup.html')

        if User.objects.filter(file_no=file_no).exists():
            messages.error(request,
                           'Your File Number, ' + file_no + ', Already Exists. Please Enter Correct File Number')
            return render(request, 'auths/user_signup.html')

        # validate password
        if password != password2:
            messages.error(request, "Your Passwords Don't match")
            return render(request, 'auths/user_signup.html')

        User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                 last_name=last_name,
                                 status=status, file_no=file_no)
        user = User.objects.get(username=username)

        context = {
            'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'status': status,
            'file_no': file_no, 'unique_id': user.unique_id
        }
        return render(request, 'auths/signup_success.html', context)
    return render(request, 'auths/user_signup.html')


# login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'This Username, ' + username + ', Does Not Exist...')
            return render(request, 'auths/login.html')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.is_superuser:
                        return redirect('/auths/display_teacher_profile/')
                    elif request.user.status == 'administrator':
                        return redirect('/auths/display_teacher_profile/')
                    elif request.user.status == 'staff - teaching':
                        return redirect('/auths/display_teacher_profile/')
                    elif request.user.status == 'staff - non-teaching':
                        return redirect('/auths/display_non_teacher_profile/')
                    elif request.user.status == 'student':
                        return redirect('/auths/display_student_profile/')
            else:
                messages.error(request, 'Username or password incorrect!!!')
                return render(request, 'auths/login.html')

    return render(request, 'auths/login.html')


# logout view
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'auths/login.html')


@login_required
def create_teacher_profile(request):
    all_zones = Zone.objects.order_by('name')
    all_schools = School.objects.order_by('zone')
    all_subjects = Subject.objects.order_by('name')
    context = {
        'all_zones': all_zones,
        'all_schools': all_schools,
        'all_subjects': all_subjects
    }

    if request.method == 'POST':
        # get all data
        title = request.POST['title']
        middle_name = request.POST['middle_name']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        age = request.POST['age']
        address = request.POST['address']
        religion = request.POST['religion']
        phone_number = request.POST['phone_number']
        picture = request.FILES['picture']
        about_me = request.POST['about_me']
        designation = request.POST['designation']
        grade_level = request.POST['grade_level']
        first_appointment = request.POST['first_appointment']
        years_in_service = request.POST['years_in_service']
        qualification = request.POST['qualification']
        discipline = request.POST['discipline']
        current_posting_zone_id = request.POST['current_posting_zone']
        current_posting_school_id = request.POST['current_posting_school']
        published_work = request.POST['published_work']
        current_subject_id = request.POST['current_subject']
        previous_posting_1_id = request.POST['previous_posting_1']
        previous_posting_2_id = request.POST['previous_posting_2']
        previous_posting_3_id = request.POST['previous_posting_3']
        other_subject_id = request.POST['other_subject']

        if previous_posting_1_id == 'Not Available':
            previous_posting_1 = None
        else:
            previous_posting_1 = School.objects.get(id=previous_posting_1_id)

        if previous_posting_2_id == 'Not Available':
            previous_posting_2 = None
        else:
            previous_posting_2 = School.objects.get(id=previous_posting_2_id)

        if previous_posting_3_id == 'Not Available':
            previous_posting_3 = None
        else:
            previous_posting_3 = School.objects.get(id=previous_posting_3_id)

        current_subject = Subject.objects.get(id=current_subject_id)
        current_posting_zone = Zone.objects.get(id=current_posting_zone_id)
        current_posting_school = School.objects.get(id=current_posting_school_id)
        other_subject = Subject.objects.get(id=other_subject_id)

        teacher = TeachingSTaff.objects.get(user=request.user)
        teacher.title = title
        teacher.middle_name = middle_name
        teacher.picture = picture
        teacher.gender = gender
        teacher.date_of_birth = date_of_birth
        teacher.age = age
        teacher.address = address
        teacher.religion = religion
        teacher.phone_number = phone_number
        teacher.about_me = about_me
        teacher.designation = designation
        teacher.grade_level = grade_level
        teacher.first_appointment = first_appointment
        teacher.years_in_service = years_in_service
        teacher.qualification = qualification
        teacher.discipline = discipline
        teacher.published_work = published_work
        teacher.current_posting_zone = current_posting_zone
        teacher.current_posting_school = current_posting_school
        teacher.previous_posting_1 = previous_posting_1
        teacher.previous_posting_2 = previous_posting_2
        teacher.previous_posting_3 = previous_posting_3
        teacher.current_subject = current_subject
        teacher.other_subject = other_subject
        teacher.save()

        images = request.FILES.getlist('documents')
        document_title = request.POST.getlist('document_title[]')
        # print(document_title, type(document_title))
        file_list = []
        for image in images:
            fs = FileSystemStorage()
            file_path = fs.save(image.name, image)
            file_list.append(file_path)

        # print(file_list, type(file_list))
        for key, value in zip(document_title, file_list):
            teacher_files = TeachingSTaffFiles(user=teacher, document_title=key, documents=value)
            teacher_files.save()
        return redirect('/auths/display_teacher_profile/')

    return render(request, 'auths/create_teacher_profile.html', context)


def add_files(request):
    if request.user.status == 'administrator' or request.user.status == 'staff - teaching':
        teacher = TeachingSTaff.objects.get(user=request.user)
        images = request.FILES.getlist('documents')
        document_title = request.POST.getlist('document_title[]')
        # print(document_title, type(document_title))
        file_list = []
        for image in images:
            fs = FileSystemStorage()
            file_path = fs.save(image.name, image)
            file_list.append(file_path)

        # print(file_list, type(file_list))
        for key, value in zip(document_title, file_list):
            teacher_files = TeachingSTaffFiles(user=teacher, document_title=key, documents=value)
            teacher_files.save()
        return redirect('/auths/display_teacher_profile/')
    elif request.user.status == 'staff - non-teaching':
        pass
    elif request.user.status == 'student':
        student = Student.objects.get(user=request.user)
        images = request.FILES.getlist('documents')
        document_title = request.POST.getlist('document_title[]')
        # print(document_title, type(document_title))
        file_list = []
        for image in images:
            fs = FileSystemStorage()
            file_path = fs.save(image.name, image)
            file_list.append(file_path)

        # print(file_list, type(file_list))
        for key, value in zip(document_title, file_list):
            student_files = StudentFiles(user=student, document_title=key, documents=value)
            student_files.save()
        return redirect('/auths/display_student_profile/')


@login_required
def display_teacher_profile(request):
    teacher = TeachingSTaff.objects.get(user=request.user)
    teacher_file = TeachingSTaffFiles.objects.filter(user=teacher)
    # count_files = len(teacher_file)

    if teacher.middle_name is None:
        messages.info(request, 'You have no profile yet. Please create your profile.')
        return HttpResponseRedirect('/auths/create_teacher_profile/')
    else:
        context = {
            'username': request.user.username, 'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email, 'status': request.user.status, 'file_no': request.user.file_no,
            'unique_id': request.user.unique_id, 'middle_name': teacher.middle_name, 'title': teacher.title,
            'picture': teacher.picture, 'gender': teacher.gender, 'date_of_birth': teacher.date_of_birth,
            'age': teacher.age, 'address': teacher.address, 'religion': teacher.religion,
            'phone_number': teacher.phone_number,
            'about_me': teacher.about_me, 'created_date': teacher.created_date, 'designation': teacher.designation,
            'grade_level': teacher.grade_level, 'first_appointment': teacher.first_appointment,
            'years_in_service': teacher.years_in_service, 'qualification': teacher.qualification,
            'discipline': teacher.discipline,
            'published_work': teacher.published_work, 'current_posting_zone': teacher.current_posting_zone,
            'current_posting_school': teacher.current_posting_school, 'previous_posting_1': teacher.previous_posting_1,
            'previous_posting_2': teacher.previous_posting_2, 'previous_posting_3': teacher.previous_posting_3,
            'current_subject': teacher.current_subject, 'other_subject': teacher.other_subject, 'teacher_file': teacher_file
        }
        return render(request, 'auths/display_teacher_profile.html', context)
    # after display profile. create a link to go to dsahboard


def teacher_docs(request):
    teacher = TeachingSTaff.objects.get(user=request.user)
    teacher_files = TeachingSTaffFiles.objects.filter(user=teacher)
    context = {
        'teacher_files': teacher_files
    }
    return render(request, 'auths/teacher_docs.html', context)


# pdf views
@login_required
def render_pdf_view(request):
    teacher = TeachingSTaff.objects.get(user=request.user)
    template_path = 'auths/render_pdf_view.html'
    context = {
        'username': request.user.username, 'first_name': request.user.first_name, 'last_name': request.user.last_name,
        'email': request.user.email, 'status': request.user.status, 'file_no': request.user.file_no,
        'unique_id': request.user.unique_id, 'middle_name': teacher.middle_name, 'title': teacher.title,
        'picture': teacher.picture, 'gender': teacher.gender, 'date_of_birth': teacher.date_of_birth,
        'age': teacher.age, 'address': teacher.address, 'religion': teacher.religion,
        'phone_number': teacher.phone_number,
        'about_me': teacher.about_me, 'created_date': teacher.created_date, 'designation': teacher.designation,
        'grade_level': teacher.grade_level, 'first_appointment': teacher.first_appointment,
        'years_in_service': teacher.years_in_service, 'qualification': teacher.qualification,
        'discipline': teacher.discipline,
        'published_work': teacher.published_work, 'current_posting_zone': teacher.current_posting_zone,
        'current_posting_school': teacher.current_posting_school, 'previous_posting_1': teacher.previous_posting_1,
        'previous_posting_2': teacher.previous_posting_2, 'previous_posting_3': teacher.previous_posting_3,
        'current_subject': teacher.current_subject, 'previous_subjects': teacher.previous_subjects,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def update_teacher_profile(request):
    teacher = TeachingSTaff.objects.get(user=request.user)
    all_zones = Zone.objects.all()
    all_schools = School.objects.order_by('zone')
    all_subjects = Subject.objects.order_by('name')

    context = {
        'teacher': teacher,
        'all_zones': all_zones,
        'all_schools': all_schools,
        'all_subjects': all_subjects
    }

    if request.method == 'POST':
        title = request.POST['title']
        middle_name = request.POST['middle_name']
        gender = request.POST['gender']
        # reg_date = request.POST['current_date_of_birth']
        # updated_date = None
        age = request.POST['age']
        address = request.POST['address']
        religion = request.POST['religion']
        phone_number = request.POST['phone_number']
        about_me = request.POST['about_me']
        designation = request.POST['designation']
        grade_level = request.POST['grade_level']

        # reg_current_first_appointment = request.POST['current_first_appointment']
        # update_first_appointment = None

        years_in_service = request.POST['years_in_service']
        qualification = request.POST['qualification']
        discipline = request.POST['discipline']

        # current_posting_zone_id = request.POST['current_posting_zone']
        # current_posting_school_id = request.POST['current_posting_school']

        published_work = request.POST['published_work']
        current_subject_id = request.POST['current_subject']
        previous_posting_1_id = request.POST['previous_posting_1']
        previous_posting_2_id = request.POST['previous_posting_2']
        previous_posting_3_id = request.POST['previous_posting_3']
        other_subject_id = request.POST['other_subject']

        if previous_posting_1_id == 'Not Available':
            previous_posting_1 = None
        else:
            previous_posting_1 = School.objects.get(id=previous_posting_1_id)

        if previous_posting_2_id == 'Not Available':
            previous_posting_2 = None
        else:
            previous_posting_2 = School.objects.get(id=previous_posting_2_id)

        if previous_posting_3_id == 'Not Available':
            previous_posting_3 = None
        else:
            previous_posting_3 = School.objects.get(id=previous_posting_3_id)

        if current_subject_id == 'Not Available':
            current_subject = teacher.current_subject
        else:
            current_subject = Subject.objects.get(id=current_subject_id)

        if other_subject_id == 'Not Available':
            other_subject = teacher.other_subject
        else:
            other_subject = Subject.objects.get(id=other_subject_id)

        y = teacher.picture
        picture = None
        try:
            if request.FILES['picture']:
                picture = request.FILES['picture']
        except:
            picture = None

        # change date format to yyyy-mm-dd for date of birth
        x = teacher.date_of_birth
        reg = x.strftime('%Y-%m-%d')

        # change date format to yyyy-mm-dd for date of appointment
        d = teacher.first_appointment
        d_reg = d.strftime('%Y-%m-%d')

        teacher.title = title
        teacher.middle_name = middle_name
        teacher.gender = gender

        try:
            if request.POST['update_date_of_birth']:
                updated_date = request.POST['update_date_of_birth']
                teacher.date_of_birth = updated_date
        except:
            teacher.date_of_birth = reg

        if picture is None:
            teacher.picture = y
        else:
            teacher.picture = picture

        teacher.age = age
        teacher.address = address
        teacher.religion = religion
        teacher.phone_number = phone_number
        teacher.about_me = about_me
        teacher.designation = designation
        teacher.grade_level = grade_level

        try:
            if request.POST['update_first_appointment']:
                update_first_appointment = request.POST['update_first_appointment']
                teacher.first_appointment = update_first_appointment
        except:
            teacher.first_appointment = d_reg

        teacher.years_in_service = years_in_service
        teacher.qualification = qualification
        teacher.discipline = discipline
        teacher.published_work = published_work

        try:
            if request.POST['current_posting_zone'] and request.POST['current_posting_school']:
                if request.POST['current_posting_zone'] == None and request.POST['current_posting_school'] == None:
                    teacher.current_posting_zone = teacher.current_posting_zone
                    teacher.current_posting_school = teacher.current_posting_school
                else:
                    current_posting_zone = Zone.objects.get(id=request.POST['current_posting_zone'])
                    current_posting_school = School.objects.get(id=request.POST['current_posting_school'])
                    teacher.current_posting_zone = current_posting_zone
                    teacher.current_posting_school = current_posting_school
        except:
            teacher.current_posting_zone = teacher.current_posting_zone
            teacher.current_posting_school = teacher.current_posting_school
        teacher.previous_posting_1 = previous_posting_1
        teacher.previous_posting_2 = previous_posting_2
        teacher.previous_posting_3 = previous_posting_3
        teacher.current_subject = current_subject
        teacher.other_subject = other_subject
        teacher.save()
        return redirect('/auths/display_teacher_profile/')
    return render(request, 'auths/update_teacher_profile.html', context)


def teaching_staff_list(request):
    all_schools = School.objects.order_by('zone')
    '''all_teachers = TeachingSTaff.objects.all().order_by('user')
    paginator = Paginator(all_teachers, 4)
    page = request.GET.get('page')
    teachers = paginator.get_page(page)'''
    context = {
        'all_schools': all_schools
    }
    return render(request, 'auths/teaching_staff_list.html', context)


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    staff = TeachingSTaff.objects.get(user=user)
    teacher_file = TeachingSTaffFiles.objects.filter(user=staff)
    context = {
        'user': user, 'staff': staff, 'teacher_file': teacher_file
    }
    return render(request, 'auths/user_profile.html', context)


def get_teachers_by_school(request):
    selected_school_id = request.GET.get('selected_school_id', None)
    selected_school = School.objects.get(id=selected_school_id)
    all_teachers = TeachingSTaff.objects.filter(current_posting_school=selected_school)
    paginator = Paginator(all_teachers, 4)
    page = request.GET.get('page')
    teachers = paginator.get_page(page)
    t = render_to_string('auths/teachers_by_school.html', {'data': teachers})
    return JsonResponse({'data': t})