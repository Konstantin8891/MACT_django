from django.contrib import admin
from django.urls import path

from api.views import SearchView

urlpatterns = [
    path('', SearchView.as_view()),
    path('admin/', admin.site.urls),
]
