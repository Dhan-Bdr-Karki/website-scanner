from django.urls import path
from .views import ScanWebsite, DisplayQueryResult

urlpatterns = [
    path('scan/', ScanWebsite.as_view(), name='scan_website'),
    path('display/', DisplayQueryResult.as_view(), name='display_result'),

]

