from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_dashboard, name='market_dashboard'),
    path('set-alert/', views.set_price_alert, name='set_price_alert'),
    path('api/realtime/', views.get_realtime_prices_api, name='realtime_prices'),
    path('check-alerts/', views.check_alerts, name='check_alerts'),
    path('delete-alert/<int:alert_id>/', views.delete_alert, name='delete_alert'),
    path('my-alerts/', views.my_alerts, name='my_alerts'),
]