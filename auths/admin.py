from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import TeachingSTaff, TeachingSTaffFiles, NonTeachingStaff, NonTeachingSTaffFiles, Zone, School, Subject, \
    Student, Class, Level, Department, StudentFiles


User = get_user_model()

class TeachingSTaffFilesInline(admin.TabularInline):
    model = TeachingSTaffFiles


class TeachingSTaffAdmin(admin.ModelAdmin):
    inlines = [TeachingSTaffFilesInline, ]


class NonTeachingSTaffFilesInline(admin.TabularInline):
    model = NonTeachingSTaffFiles


class NonTeachingSTaffAdmin(admin.ModelAdmin):
    inlines = [NonTeachingSTaffFilesInline, ]


class StudentFilesInline(admin.TabularInline):
    model = StudentFiles


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentFilesInline, ]


admin.site.register(TeachingSTaff, TeachingSTaffAdmin)
admin.site.register(NonTeachingStaff, NonTeachingSTaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Zone)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Level)
admin.site.register(TeachingSTaffFiles)
admin.site.register(NonTeachingSTaffFiles)

admin.site.site_header = 'School Management Admin'