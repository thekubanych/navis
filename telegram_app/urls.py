from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from .views import (VacancyViewSet, ApplicationViewSet, WeSelfViewSet,FreeConsultationViewSet,
                    DesignPageViewSet, AllProjectViewSet,EventViewSet)


router = DefaultRouter()
router.register(r'vacancies', views.VacancyViewSet, basename='vacancy')
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'WeSelf', WeSelfViewSet)
router.register(r'free-consultation', FreeConsultationViewSet, basename='free-consultation')
router.register(r'design', DesignPageViewSet)
router.register(r'all-projects', AllProjectViewSet)
router.register(r'events', EventViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="IT Studio API",
        default_version='v1',
        description='dokumentatsiya api dlya vakansiy i zayavok',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('posts/', views.get_posts, name='get_posts'),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('', include(router.urls)),

]
