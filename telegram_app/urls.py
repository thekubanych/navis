from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from .views import (
    VacancyViewSet, ApplicationViewSet, WeSelfViewSet, FreeConsultationViewSet,
    DesignPageViewSet, AllProjectViewSet, EventViewSet, RegisterViewSet
)

router = DefaultRouter()
router.register(r'vacancies', VacancyViewSet, basename='vacancy')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'weself', WeSelfViewSet, basename='weself')
router.register(r'free-consultation', FreeConsultationViewSet, basename='free-consultation')
router.register(r'design', DesignPageViewSet, basename='design')
router.register(r'all-projects', AllProjectViewSet, basename='all-projects')
router.register(r'events', EventViewSet, basename='events')
router.register(r'register', RegisterViewSet, basename='register')


schema_view = get_schema_view(
    openapi.Info(
        title="IT Studio API",
        default_version='v1',
        description='Документация API для вакансий и заявок',
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
]
