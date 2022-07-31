from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('login/', views.loginPage, name="login"),
    path('login-first/', views.loginFirstPage, name="login-first"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
   
    path('tasks/', views.tasks, name="tasks"),
    path('task/<pk>/', views.taskDetail, name="task"),
    path('tasks-completed/', views.tasksCompleted, name="tasks-completed"),
    path('tasks-due/', views.tasksDue, name="tasks-due"),
    path('add-task/', views.addTask, name="add-task"),
    path('edit-task/<pk>', views.editTask, name="edit-task"),
    path('complete-task/<pk>/', views.completeTask, name="complete-task"),
    path('delete-task/<pk>', views.deleteTask, name="delete-task"),

    path('members/', views.members, name="members"),
    path('add-member/', views.addmember, name="add-member"),
    path('member/<pk>', views.member, name='member'),
    path('profile', views.profile, name='profile'),
    path('profile-settings', views.profileSettings, name='profile-settings'),
    path('edit-member/<pk>', views.editmember, name='edit-member'),

    path('activities/', views.activities, name="activities"),
    path('add-activity/', views.addActivity, name="add-activity"),
    path('complete-activity/<pk>/', views.completeActivity, name="complete-activity"),
    path('delete-activity/<pk>/', views.deleteActivity, name="delete-activity"),

    path('user-request/<pk>/', views.userRequest, name='user-request'),
    path('submit-request/', views.submitRequest, name='submit-request'),
    path('resolve-request/<pk>/', views.resolveRequest, name='resolve-request'),
    path('delete-request/<pk>/', views.deleteRequest, name='delete-request'),
    path('user-requests/', views.userRequests, name="user-requests"),

    path('projects/',views.projects, name='projects'),
    path('project/<pk>/',views.project, name='project'),
    path('add-project/', views.addProject, name='add-project'),
    path('delete-project/<pk>', views.deleteProject, name='delete-project'),
    path('edit-project/<pk>', views.editProject, name='edit-project'),
    path('complete-project/<pk>', views.completeProject, name='complete-project'),
    path('uncomplete-project/<pk>', views.uncompleteProject, name='uncomplete-project')
]