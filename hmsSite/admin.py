from django.contrib import admin, messages
from django.utils.translation import ngettext
# Register your models here.

from .models import ArchivedProject, Project, School, Faculty, Image_Stock
import os

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'approved']
    list_editable = ['approved']
    list_filter = ['faculty', 'school', 'approved']
    search_fields = ['title', 'contact1_name', 'contact2_name']
    ordering = ['approved']
    actions = ['approve', 'archive']

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data:
            obj = form.save(commit=False)
            obj.save_form()
        super().save_model(request, obj, form, change)

    def approve(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, ngettext(
            '%d project was successfully approved.',
            '%d projects were successfully approved.',
            updated,
        ) % updated, messages.SUCCESS)
        for proj in queryset:
            if os.environ.get('DJANGO_ENV') == 'production':
                reversedUrl = f'https://researchprojectsdemo.azurewebsites.net/project/{proj.id}/'
            else:
                reversedUrl = f'http://127.0.0.1:8000/project/{proj.id}/'
            proj.user.email_user(
                f'Your project - {proj.title} - has been approved',
                f'Hello {proj.user.get_full_name()},\r\n\r\nYour project has been approved by a moderator. You can view your project at {reversedUrl}.\r\n\r\nThis is an automated email. Please do not reply to it.',
                ''
            )
    approve.short_description = "Approve selected projects"

    def archive(self, request, queryset):
        for proj in queryset:
            proj.archive()
        self.message_user(request,'Project was successfully archived')
    archive.short_description = "Archive selected projects"

class ArchivedProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'approved']
    list_editable = ['approved']
    list_filter = ['faculty', 'school', 'approved']
    search_fields = ['title', 'contact1_name', 'contact2_name']
    ordering = ['approved']
    actions = ['unarchive']

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data:
            obj = form.save(commit=False)
            obj.save_form()
        super().save_model(request, obj, form, change)

    def unarchive(self, request, queryset):
        for proj in queryset:
            proj.archive()
        self.message_user(request,'Project was successfully unarchived')
    unarchive.short_description = "Unarchive selected projects"



admin.site.register(School)
admin.site.register(Faculty)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Image_Stock)
admin.site.register(ArchivedProject, ArchivedProjectAdmin)
