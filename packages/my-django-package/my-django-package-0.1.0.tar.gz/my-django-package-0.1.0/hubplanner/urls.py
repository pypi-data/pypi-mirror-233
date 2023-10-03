from django.urls import path
from . import views

urlpatterns = [
    path('importdata/',views.importHubplannerData),
    path('updatedepartmentalhours/',views.addOrUpdateDepartmentalHoursToHubplanner),
    path('getepartmentalhours/',views.getDepartmentalHoursToHubplanner)
]