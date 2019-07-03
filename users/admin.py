from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.admin import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from .models import User, Card, Temporary, Invitation


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'number', 'password', 'wallet')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'number', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'number', 'email', 'first_name', 'last_name', 'wallet', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'number')
    ordering = ('number', 'username')
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    list_display = ('get_username', 'name', 'idm', 'is_guest')

    def get_username(self, obj: Card):
        return obj.user.username
    get_username.short_description = 'ユーザー名'


@admin.register(Temporary)
class TemporaryAdmin(ImportExportModelAdmin):
    list_display = ('idm', 'uuid')


@admin.register(Invitation)
class InvitationAdmin(ImportExportModelAdmin):
    list_display = ('uuid', 'is_active', 'generated_time')

    def get_urls(self):
        urls = super().get_urls()
        extend_urls = [
            path('manage/', self.admin_site.admin_view(self.manage_invitation))
        ]
        return extend_urls + urls

    def manage_invitation(self, request):
        invitations = Invitation.objects.all()
        context = dict(
            self.admin_site.each_context(request),
        )
        context['invitations'] = invitations

        if request.method == 'POST':
            invitation = Invitation()
            invitation.save()
            invitation_url = str(request.scheme) + "://" + str(request.get_host()) + '/accounts/signup/' + str(invitation.uuid) + '/'
            context['invitation_url'] = invitation_url
            return render(request, 'admin/users/invitation/manage_invitation.html', context)

        return render(request, 'admin/users/invitation/manage_invitation.html', context)
