from django.contrib import admin
from .models import Project, Task, Activity, Member, MemberRequest

# Register your models here.

admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Activity)
admin.site.register(MemberRequest)