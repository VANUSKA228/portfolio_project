from django.urls import path
from . import views
from accounts.views import logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('api/search/', views.search_users_api, name='search_users_api'),
    path('user/<str:username>/', views.user_public_profile, name='user_public_profile'),
    path('dashboard/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('dashboard/bulk-delete/', views.admin_bulk_delete, name='admin_bulk_delete'),
    path('dashboard/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('dashboard/impersonate/<int:user_id>/', views.admin_impersonate, name='admin_impersonate'),
    path('dashboard/restore/', views.admin_restore, name='admin_restore'),
    path('accounts/logout/', logout_view, name='logout'),
]