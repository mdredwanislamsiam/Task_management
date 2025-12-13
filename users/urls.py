from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard,  assign_role, create_group, group_list, CustomLoginView, ProfileView, CustomLogoutView, CustomChangePasswordView, CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView, SignUpView, AdminDashboard, GroupListView, CreateGroupView, AssignRole
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView


urlpatterns = [
#     path('sign_up/', sign_up, name='sign_up'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    # path('sign_in/', sign_in, name='sign_in'),
    path('sign_in/', CustomLoginView.as_view(), name='sign_in'),
    # path('sign_out/', sign_out, name="sign_out"),
    path('sign_out/', CustomLogoutView.as_view(), name="sign_out"),
    path('activate/<int:user_id>/<str:token>/', activate_user),
#     path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
    # path('admin/<int:user_id>/assign_role/', assign_role, name='assign_role'),
    path('admin/<int:user_id>/assign_role/', AssignRole.as_view(), name='assign_role'),
    # path('admin/create_group/', create_group, name='create_group'),
    path('admin/create_group/', CreateGroupView.as_view(), name='create_group'),
    # path('admin/group_list/', group_list, name='group_list'),
    path('admin/group_list/', GroupListView.as_view(), name='group_list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/', CustomChangePasswordView.as_view(),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'), 
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit_profile', EditProfileView.as_view(), name = 'edit_profile')
    
]
