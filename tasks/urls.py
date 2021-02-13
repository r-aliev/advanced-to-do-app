from django.urls import path



from . import views

app_name = 'tasks'
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),

    path('', views.index, name="index"),
    path('detail/<int:pk>/', views.detail, name="detail"),
    path('update/<str:pk>/', views.update, name="update"),
    path('delete/<int:pk>/', views.delete, name="delete"),
    path('share/<int:pk>/', views.share, name="share"),
]


