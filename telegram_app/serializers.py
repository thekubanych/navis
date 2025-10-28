from rest_framework import serializers
from .models import Post, Vacancy, Application, WeSelf, FreeConsultation, DesignPage, AllProject, Event


# ux ui
class DesignPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignPage
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'img', 'title', 'description', 'ckeditor']
# vakansiya
class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

# zayavka
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class WeSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeSelf
        fields = '__all__'


class FreeConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeConsultation
        fields = '__all__'


#  vseh project
class AllProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllProject
        fields = '__all__'

# meropriyatiya

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'