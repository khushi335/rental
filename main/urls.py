from django.urls import path
from . import views, views_api

urlpatterns = [
    path('', views.index, name='index'),
    path('index-landlord',views.index_landlord,name="index_landlord"),
    path('about_us/',views.about_us,name='about_us'),
    path('contact/',views.contact,name="contact"),
    path('contact-landlord/',views.contact_landlord,name="contact_landlord"),
    path('category/<int:category_id>/', views.property_list_by_category, name='property_list_by_category'),
    path('find/', views.find_me_room, name='find_me_room'),
    path('shift-home/', views.shift_home, name='shift_home'),
    path('reviews/', views.user_reviews, name='user_reviews'),
    path('shift-success/', views.shift_success, name='shift_success'),
    path('tenant-shift-dashboard/', views.tenant_shift_dashboard, name='tenant_shift_dashboard'),
    path('properties/', views.property_list, name='property_list'),
    path('properties-landlord/', views.property_list_landlord, name='property_list_landlord'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('add_property/', views.add_property, name='add_property'),
    path('edit_property/<int:pk>/', views.edit_property, name='edit_property'),
    path('delete_property/<int:pk>/', views.delete_property, name='delete_property'),
    path('favorite_list/', views.favorite_list, name='favorite_list'),
    path('toggle_favorite/<int:property_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('landlord_dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('tenant_dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('add_review/<int:property_id>/', views.add_or_update_review, name='add_or_update_review'),
    path('delete_review/<int:property_id>/', views.delete_review, name='delete_review'),
    path('landlord/inquiries/', views.landlord_inquiries, name='landlord_inquiries'),
    path('property/<int:property_id>/report/', views.report_property, name='report_property'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('settings/', views.settings, name='settings'),


    # API views
    path('api/properties/', views_api.PropertyListCreateAPIView.as_view(), name='api_property_list_create'),
    path('api/properties/<int:pk>/', views_api.PropertyDetailAPIView.as_view(), name='api_property_detail'),
    path('api/favorite_toggle/<int:property_id>/', views_api.FavoriteToggleAPIView.as_view(), name='api_favorite_toggle'),
    path('api/favorites/', views_api.FavoriteListAPIView.as_view(), name='api_favorites'),
    path('api/review/<int:property_id>/', views_api.AddOrUpdateReviewAPIView.as_view(), name='api_add_update_review'),
    path('api/review/<int:property_id>/delete/', views_api.DeleteReviewAPIView.as_view(), name='api_delete_review'),
]


