from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Vacancy, Application, Post, WeSelf, FreeConsultation, DesignPage, AllProject, Event
from .serializers import VacancySerializer, ApplicationSerializer, PostSerializer,WeSelfSerializer,FreeConsultationSerializer, DesignPageSerializer,AllProjectSerializer, EventSerializer
import requests
import random

# class AllProjectViewSet(viewsets.)


class DesignPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignPage.objects.all().order_by('-created_at')
    serializer_class = DesignPageSerializer



# Telegram bot
TOKEN = '8280608817:AAG2-VAQv7SzrhI5xQ7ev4MmM_njfDzCtto'
GROUP_ID = '-1003082347664'

# --- ViewSets для API ---
class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        # Проверка обязательных полей
        required_fields = ['name', 'phone', 'email', 'vacancy']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'status': 'fail', 'error': f'{field} is required'},
                    status=400
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Формируем сообщение для Telegram
        message = (
            f"📩 Новая заявка на вакансию:\n"
            f"Вакансия: {instance.vacancy.title}\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"LinkedIn: {instance.linkedin or 'нет'}"
        )

        # Отправка в Telegram с обработкой ошибок
        try:
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            response = requests.post(url, data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
            if response.status_code != 200:
                print(f"Telegram error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Telegram exception: {e}")

        return Response({'status': 'ok', 'application_id': instance.id}, status=201)


#  polucheniya postov ---
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# -otpravka zayavki na telegram
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def send_message(request):
    try:
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not email or not phone:
            return Response({'status': 'fail', 'error': 'email and phone number obezyatelno'}, status=400)

        code = random.randint(100000, 999999)
        message = f"📩 Новая заявка:\nEmail: {email}\nPhonenumber: {phone}\ncode verification: {code}"

        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {'chat_id': GROUP_ID, 'text': message}
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            return Response({'status': 'ok', 'code': code})
        else:
            return Response({'status': 'fail', 'error': response.text}, status=500)

    except Exception as e:
        return Response({'status': 'error', 'details': str(e)}, status=500)



class WeSelfViewSet(viewsets.ModelViewSet):
    """API для управления страницей 'О нас'"""
    queryset = WeSelf.objects.all()
    serializer_class = WeSelfSerializer



class FreeConsultationViewSet(viewsets.ModelViewSet):
    queryset = FreeConsultation.objects.all()
    serializer_class = FreeConsultationSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        message = (
            f"📞 new consultation:\n"
            f"name: {instance.name}\n"
            f"phone: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"address: {instance.address}\n"
            f"rejim rabotu: {instance.house_working}"
        )
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(url, data={'chat_id': GROUP_ID, 'text': message})


class AllProjectViewSet(viewsets.ModelViewSet):
    queryset = AllProject.objects.all()
    serializer_class = AllProjectSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
