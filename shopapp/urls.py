from django.urls import path
from shopapp import views, HodViews, StaffViews, BidhaaViews
from shop import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication URLs
    path('', views.ShowLoginPage, name='show_login'),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),
    
    # Admin Home
    path('admin_home', HodViews.admin_home, name="admin_home"),
    
    # Staff Management
    path('add_staff', HodViews.add_staff, name="add_staff"),
    path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
    path('manage_staff', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
    
    # Course Management
    path('add_course', HodViews.add_course, name="add_course"),
    path('add_course_save', HodViews.add_course_save, name="add_course_save"),
    path('manage_course', HodViews.manage_course, name="manage_course"),
    
    # Subject Management
    path('add_subject', HodViews.add_subject, name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_subject', HodViews.manage_subject, name="manage_subject"),
    
    # Bidhaa Management - CORRECTED URLs
    path('add_bidhaa/', HodViews.add_bidhaa, name="add_bidhaa"),
    path('add_bidhaa_save/', HodViews.add_bidhaa_save, name="add_bidhaa_save"),
    path('manage_bidhaa/', HodViews.manage_bidhaa, name="manage_bidhaa"),
    path('edit_bidhaa/<int:bidhaa_id>/', HodViews.edit_bidhaa, name="edit_bidhaa"),
    path('edit_bidhaa_save/', HodViews.edit_bidhaa_save, name="edit_bidhaa_save"),  # CHANGED - No ID needed
    path('view_bidhaa/<int:bidhaa_id>/', HodViews.view_bidhaa, name="view_bidhaa"),
    path('delete_bidhaa/<int:bidhaa_id>/', HodViews.delete_bidhaa, name="delete_bidhaa"),
    
    # Additional Bidhaa URLs
    path('low_stock_alert/', HodViews.low_stock_alert, name='low_stock_alert'),
    path('bidhaa_statistics/', HodViews.bidhaa_statistics, name='bidhaa_statistics'),
    path('bulk_update_quantities/', HodViews.bulk_update_quantities, name='bulk_update_quantities'),
    path('export_bidhaa_csv/', HodViews.export_bidhaa_csv, name='export_bidhaa_csv'),
    
    # AJAX endpoints (optional)
    path('ajax/get_bidhaa_details/<int:bidhaa_id>/', HodViews.get_bidhaa_details, name='get_bidhaa_details'),
    path('ajax/check_code_exists/', HodViews.check_code_exists, name='check_code_exists'),

    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('check_email_exist', HodViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    path('staff_feedback_message', HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('staff_leave_view', HodViews.staff_leave_view,name="staff_leave_view"),
    path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave,name="staff_approve_leave"),
    path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('admin_profile', HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save,name="admin_profile_save"),
    path('send_staff_notification', HodViews.send_staff_notification,name="send_staff_notification"),
    

#     Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),

#     bidhaa URL Path
    path('bidhaa_home', BidhaaViews.bidhaa_home, name="bidhaa_home"),
    path('bidhaa_profile', BidhaaViews.bidhaa_profile, name="bidhaa_profile"),
    path('bidhaa_profile_save', BidhaaViews.bidhaa_profile_save, name="bidhaa_profile_save"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
