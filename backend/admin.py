from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from backend.models import (Mailing, MailingLink, User, UserMailingForm,
                            ProfileStatistics)


class MailingAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), label='Текст')


class UserMailingFormAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(), label='Текст')


class MailingLinkInlineAdmin(admin.TabularInline):
    model = MailingLink
    extra = 1


class UserMailingFormInlineAdmin(admin.StackedInline):
    model = UserMailingForm
    extra = 0
    form = UserMailingFormAdminForm


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']
    form = MailingAdminForm
    inlines = [MailingLinkInlineAdmin]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'mailing', 'info', 'created', 'updated']
    search_fields = ['profile']
    list_filter = ['mailing']
    inlines = [UserMailingFormInlineAdmin]


@admin.register(ProfileStatistics)
class ProfileStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'get_applications_count',
                    'get_adopted_count', 'get_unaccepted_count', 
                     'get_adopted_percentage']
