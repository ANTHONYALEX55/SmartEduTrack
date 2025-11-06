from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id','student','date','status','marked_by']
@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'standard']
    
@admin.register(ParentStudent)
class ParentStudentAdmin(admin.ModelAdmin):
    list_display = ['parent','student']
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'standard', 'section', 'created_at']
    
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id','name','code','standard','teacher']