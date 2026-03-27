from django.urls import  path
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    #path('prediction',views.predPage,name="predict"),
    path('logout',views.logout,name='logout'),
    path('data',views.predict,name='data'),
    path("analysis/", views.detailed_analysis, name="analysis"),
    path("api/predict/", views.api_predict, name="api_predict")
]