import random
import string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone

User = settings.AUTH_USER_MODEL


def random_code(digit=7, letter=3):
    sample_str = ''.join((random.choice(string.digits) for i in range(digit)))
    sample_str += ''.join((random.choice(string.ascii_uppercase) for i in range(letter)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string


class CustomUser(AbstractUser):
    unique_id = models.CharField(default=random_code, max_length=10, unique=True)
    STATUS = [
        ('administrator', 'administrator'),
        ('staff - teaching', 'staff - teaching'),
        ('staff - non-teaching', 'staff - non-teaching'),
        ('student', 'student'),
    ]
    status = models.CharField(default=STATUS[0], choices=STATUS, max_length=20)
    file_no = models.CharField(max_length=100, unique=True)


def teachers_directory(instance, filename):
    return f'Teachers_Files/{instance.user.first_name}_{instance.user.last_name}/'


def non_teachers_directory(instance, filename):
    return f'Non_Teachers_Files/{instance.user.first_name}_{instance.user.last_name}/'


def students_directory(instance, filename):
    return f'Students_Files/{instance.user.first_name}_{instance.user.last_name}/'


class Zone(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'

    def __str__(self):
        return self.name


class School(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)

    class Meta:
        ordering = ('id',)
        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __str__(self):
        return f'{self.name} | {self.zone.name}'


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department

    class Meta:
        ordering = ('id',)
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class Level(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level

    class Meta:
        ordering = ('id',)
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'


class TeachingSTaff(models.Model):
    DESIGNATION = [
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Head of Department', 'Head of Department'),
        ('Subject Teacher', 'Subject Teacher'),
    ]

    TITLE = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
    ]

    QUALIFICATION = [
        ('NCE', 'NCE'),
        ('HND', 'HND'),
        ('B.Sc', 'B.Sc'),
        ('PGDE', 'PGDE'),
        ('B.Arts', 'B.Arts'),
        ('M.Sc', 'M.Sc'),
        ('PhD', 'PhD'),
    ]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    RELIGION = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Others', 'Others'),
    ]
    # general data
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(choices=TITLE, max_length=10, null=True)
    middle_name = models.CharField(max_length=25, help_text='Enter your middle name here if any', null=True)
    picture = models.ImageField(upload_to='Teachers_Photo/%Y/%m/%d/', null=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=300, null=True)
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # work related info
    designation = models.CharField(choices=DESIGNATION, max_length=100)
    grade_level = models.CharField(max_length=20, help_text='E.g, Level 8 Step 2', null=True)
    first_appointment = models.DateField(null=True)
    years_in_service = models.CharField(max_length=15, null=True)
    qualification = models.CharField(choices=QUALIFICATION, max_length=10, null=True)
    discipline = models.CharField(max_length=200, null=True)
    published_work = models.URLField(max_length=200, help_text='Start with "http://" or https://', null=True)
    current_posting_zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='zone', null=True)
    current_posting_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='current', null=True)
    previous_posting_1 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='posting_1', null=True)
    previous_posting_2 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='posting_2', null=True)
    previous_posting_3 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='posting_3', null=True)
    current_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='current', null=True)
    other_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='other', null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Teaching Staff'
        verbose_name_plural = 'Teaching Staffs'

    def __str__(self):
        return f'Profile of {self.user.first_name} {self.user.last_name}'


class TeachingSTaffFiles(models.Model):
    user = models.ForeignKey(TeachingSTaff, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=100)
    documents = models.FileField(upload_to='Teachers_Files/%Y/%m/%d/')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Teaching Staff File'
        verbose_name_plural = 'Teaching Staff Files'

    def __str__(self):
        return f'Files for {self.user.title} {self.user.user.last_name}'


class NonTeachingStaff(models.Model):
    DESIGNATION = [
        ('Office Assistant', 'Office Assistant'),
        ('Secretary', 'Secretary'),
        ('Librarian', 'Librarian'),
        ('Others', 'Others'),
    ]

    TITLE = [
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
    ]

    QUALIFICATION = [
        ('SSCE', 'SSCE'),
        ('OND', 'OND'),
        ('HND', 'HND'),
        ('PGDE', 'PGDE'),
        ('B.Sc', 'B.Sc'),
        ('B.Arts', 'B.Arts'),
    ]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    RELIGION = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Others', 'Others'),
    ]
    # general data
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(choices=TITLE, max_length=10, null=True)
    middle_name = models.CharField(max_length=25, help_text='Enter your middle name here if any', null=True)
    picture = models.ImageField(upload_to='Non_Teachers_Photo/%Y/%m/%d/', null=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=300, null=True)
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words',
                                null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # work related info
    designation = models.CharField(choices=DESIGNATION, max_length=100)
    grade_level = models.CharField(max_length=20, help_text='E.g, Level 8 Step 2')
    first_appointment = models.DateField(null=True)
    years_in_service = models.CharField(max_length=15, null=True)
    qualification = models.CharField(choices=QUALIFICATION, max_length=10, null=True)
    discipline = models.CharField(max_length=200, null=True)
    current_posting_zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='zones', null=True)
    current_posting_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='currents', null=True)
    previous_posting_1 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='postings_1', null=True)
    previous_posting_2 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='postings_2', null=True)
    previous_posting_3 = models.ForeignKey(School, on_delete=models.CASCADE, related_name='postings_3', null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Non Teaching Staff'
        verbose_name_plural = 'Non Teaching Staffs'

    def __str__(self):
        return f'Profile of {self.user.first_name} {self.user.last_name}'


class NonTeachingSTaffFiles(models.Model):
    user = models.ForeignKey(NonTeachingStaff, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=100)
    documents = models.FileField(upload_to='Non_Teachers_Files/%Y/%m/%d/')

    def __str__(self):
        return f'Files for {self.user.title} {self.user.user.last_name}'


class Student(models.Model):

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    RELIGION = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Others', 'Others'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=25, help_text='Enter your middle name here if any', null=True)
    admission_year = models.CharField(max_length=100, null=True)
    current_school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Name of current school', null=True, related_name='school')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    std_class = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Class', null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    prev_school_1 = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Former school 1', null=True, related_name='school_1')
    prev_school_2 = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Former school 1', null=True, related_name='school_2')
    prev_school_3 = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Former school 1', null=True, related_name='school_3')
    picture = models.ImageField(upload_to='Student_Photo/%Y/%m/%d/', null=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True)
    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=300, null=True)
    religion = models.CharField(choices=RELIGION, max_length=20, null=True)
    student_phone_number = models.CharField(max_length=20, null=True)
    father_name = models.CharField(max_length=10, null=True, verbose_name="Father's Full Name")
    father_phone = models.CharField(max_length=10, null=True, verbose_name="Father's Phone Number")
    father_img = models.ImageField(upload_to='Parents_Fathers/%Y/%m/%d/', null=True)
    mother_name = models.CharField(max_length=10, null=True, verbose_name="Mother's Full Name")
    mother_phone = models.CharField(max_length=10, null=True, verbose_name="Mother's Phone Number")
    mother_img = models.ImageField(upload_to='Parents_Mothers/%Y/%m/%d/', null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'Profile of {self.user.first_name} {self.user.last_name}'


class StudentFiles(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=100)
    documents = models.FileField(upload_to='Student_files/%Y/%m/%d/')

    def __str__(self):
        return f'Files for {self.user.user.first_name} {self.user.user.last_name}'


def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        if instance.status == 'administrator':
            TeachingSTaff.objects.create(user=instance)
        if instance.status == 'staff - teaching':
            TeachingSTaff.objects.create(user=instance)
        if instance.status == 'staff - non-teaching':
            NonTeachingStaff.objects.create(user=instance)
        if instance.status == 'student':
            Student.objects.create(user=instance)


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)