from django.urls import path
from . import views

urlpatterns = [
    path('accounts/',views.getAccounts),
    path('accounts/getSobjects/', views.getSobjects),
    path('accounts/getFieldName/<sobject>/', views.getFieldName),
    # path('getAllOpportunity/', views.OpportunityListView.as_view()),
    path('getAllOpportunity/', views.getOpportunity),
    path('insertOpportunity/', views.AddOrUpdateOpportunity),
    path('getOpportunity/', views.getNewOpportunity)
]