from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Vacancy, Application, Post, WeSelf, FreeConsultation, DesignPage, AllProject, Event, Register
from .serializers import VacancySerializer, ApplicationSerializer, PostSerializer, WeSelfSerializer, FreeConsultationSerializer, DesignPageSerializer, AllProjectSerializer, EventSerializer, RegisterSerializer
import requests
import random




# Telegram bot
TOKEN = '8280608817:AAG2-VAQv7SzrhI5xQ7ev4MmM_njfDzCtto'
GROUP_ID = '-1003082347664'


# ------------------- VIEWSETS -------------------

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.AllowAny]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        required_fields = ['name', 'phone', 'email', 'vacancy']
        missing_fields = [f for f in required_fields if not data.get(f)]
        if missing_fields:
            return Response({'status': 'fail', 'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Telegram message
        vacancy_title = getattr(instance.vacancy, 'title', 'Не указано')
        message = (
            f"📩 Новая заявка на вакансию:\n"
            f"Вакансия: {vacancy_title}\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"LinkedIn: {instance.linkedin or 'нет'}"

        )
        try:
            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        except Exception as e:
            print(f"Telegram exception: {e}")

        return Response({'status': 'ok', 'application_id': instance.id}, status=201)


class WeSelfViewSet(viewsets.ModelViewSet):
    queryset = WeSelf.objects.all()
    serializer_class = WeSelfSerializer
    permission_classes = [permissions.AllowAny]


class FreeConsultationViewSet(viewsets.ModelViewSet):
    queryset = FreeConsultation.objects.all()
    serializer_class = FreeConsultationSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        message = (
            f"📞 Новая консультация:\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"Адрес: {instance.address}\n"
            f"Режим работы: {instance.house_working}"
        )
        try:
            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        except Exception as e:
            print(f"Telegram exception: {e}")


class DesignPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignPage.objects.all().order_by('-created_at')
    serializer_class = DesignPageSerializer
    permission_classes = [permissions.AllowAny]


class AllProjectViewSet(viewsets.ModelViewSet):
    queryset = AllProject.objects.all()
    serializer_class = AllProjectSerializer
    permission_classes = [permissions.AllowAny]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        message = (
            f"📌 Новая регистрация:\n"
            f"Имя: {instance.username}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email}"
        )
        try:
            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        except Exception as e:
            print(f"Telegram exception: {e}")


# ------------------- API ФУНКЦИИ -------------------

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def send_message(request):
    try:
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not email or not phone:
            return Response({'status': 'fail', 'error': 'email and phone обязательны'}, status=400)

        code = random.randint(100000, 999999)
        message = f"📩 Новая заявка:\nEmail: {email}\nPhone: {phone}\nCode: {code}"

        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        if response.status_code == 200:
            return Response({'status': 'ok', 'code': code})
        return Response({'status': 'fail', 'error': response.text}, status=500)

    except Exception as e:
        return Response({'status': 'error', 'details': str(e)}, status=500)
