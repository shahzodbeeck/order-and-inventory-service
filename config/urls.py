from django.urls import include, path

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("", include("apps.products.urls")),
    path("", include("apps.orders.urls")),
]
