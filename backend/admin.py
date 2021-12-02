from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from backend.models import Mailing, User, MailingLink


class MailingAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), label='Текст')


class UserAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(), label='Текст')


class MailingLinkInlineAdmin(admin.TabularInline):
    model = MailingLink
    extra = 1


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']
    form = MailingAdminForm
    inlines = [MailingLinkInlineAdmin]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'mailing_link', 'screenshot_link', 'created', 'updated']
    form = UserAdminForm
