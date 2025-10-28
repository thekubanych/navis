from .models import Post, Vacancy, Application, WeSelf,  FreeConsultation
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from .models import DesignPage

@admin.register(DesignPage)
class DesignPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(FreeConsultation)
class FreeConsultationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'house_working')

# CKEditor для Post
class PostAdminForm(forms.ModelForm):
    ckeditor = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)
admin.site.register(Vacancy)
admin.site.register(Application)
admin.site.register(WeSelf)
