from django.urls import path, include

urlpatterns = [
    path('', include(('hotel.urls.admin_urls', 'hotel'), namespace='hotel')),      # 관리자용
    path('', include(('hotel.urls.customer_urls', 'customer'), namespace='customer')),  # 고객용
]
