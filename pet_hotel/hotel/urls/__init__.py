from django.urls import include, path

urlpatterns = [
    path('hotel/', include('hotel.urls.admin_urls')),
    path('hotel/', include('hotel.urls.customer_urls')),
]
