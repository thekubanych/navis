import re
import random
import requests
from rest_framework import viewsets, permissions, status, serializers, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
# Telegram bot
TOKEN = '8280608817:AAG2-VAQv7SzrhI5xQ7ev4MmM_njfDzCtto'
GROUP_ID = '-1003082347664'

# Регулярки для валидации
PHONE_REGEX = re.compile(r'^\+996\d{9}$')
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')




# -------------------- ViewSets -------------------- #

class DesignPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignPage.objects.all().order_by('-created_at')
    serializer_class = DesignPageSerializer


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):  # Только GET
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

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
            return Response(
                {'status': 'fail', 'error': f'Missing fields: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone = data.get('phone')
        email = data.get('email')

        if not PHONE_REGEX.match(phone):
            return Response({'status': 'fail', 'error': 'Invalid phone number. Use +996XXXXXXXXX'}, status=400)
        if not EMAIL_REGEX.match(email):
            return Response({'status': 'fail', 'error': 'Invalid email format'}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Формируем текстовое сообщение
        vacancy_title = getattr(instance.vacancy, 'title', 'Не указано')
        message = (
            f"📩 Новая заявка на вакансию:\n"
            f"Вакансия: {vacancy_title}\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email}\n"
            f"LinkedIn: {instance.linkedin or 'нет'}"
        )

        # Отправка текста
        try:
            requests.post(
                f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                data={'chat_id': GROUP_ID, 'text': message},
                timeout=5
            )
        except Exception as e:
            print(f"Telegram exception: {e}")

        # Отправка файла, если он есть
        if instance.file:
            try:
                with open(instance.file.path, 'rb') as f:
                    requests.post(
                        f'https://api.telegram.org/bot{TOKEN}/sendDocument',
                        data={'chat_id': GROUP_ID},
                        files={'document': f},
                        timeout=10
                    )
            except Exception as e:
                print(f"Telegram file exception: {e}")

        return Response({'status': 'ok', 'application_id': instance.id}, status=201)
# -------------------- Получение постов -------------------- #
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# -------------------- Отправка заявки на Telegram -------------------- #
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def send_message(request):
    email = request.data.get('email')
    phone = request.data.get('phone')

    if not email or not phone:
        return Response({'status': 'fail', 'error': 'Email and phone are required'}, status=400)
    if not PHONE_REGEX.match(phone):
        return Response({'status': 'fail', 'error': 'Invalid phone number. Use +996XXXXXXXXX'}, status=400)
    if not EMAIL_REGEX.match(email):
        return Response({'status': 'fail', 'error': 'Invalid email format'}, status=400)

    code = random.randint(100000, 999999)
    message = f"📩 Новая заявка:\nEmail: {email}\nТелефон: {phone}\nКод верификации: {code}"

    try:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                      data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
    except Exception as e:
        print(f"Telegram exception: {e}")

    return Response({'status': 'ok', 'code': code})


# -------------------- О нас -------------------- #
class WeSelfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeSelf.objects.all()
    serializer_class = WeSelfSerializer
    permission_classes = [permissions.AllowAny]

# -------------------- FreeConsultation -------------------- #

NAME_REGEX = re.compile(r'^[A-Za-zА-Яа-яЁё]+$')
class FreeConsultationViewSet(viewsets.ModelViewSet):
    queryset = FreeConsultation.objects.all()
    serializer_class = FreeConsultationSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Валидация
        if not PHONE_REGEX.match(instance.phone):
            raise serializers.ValidationError({'phone': 'Invalid phone number. Use +996XXXXXXXXX'})

        if instance.email and not EMAIL_REGEX.match(instance.email):
            raise serializers.ValidationError({'email': 'Invalid email format'})
        if not NAME_REGEX.match(instance.name):
            raise serializers.ValidationError({'name': 'Name must contain only letters'})



        # Telegram
        message = (
            f"📞 Новая консультация:\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email or 'нет'}\n"
            f"Адрес: {instance.address}\n"
            f"Время работы: {instance.house_working}"
        )
        try:
            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                          data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        except Exception as e:
            print(f"Telegram exception: {e}")


# -------------------- AllProject -------------------- #
class AllProjectViewSet(viewsets.ReadOnlyModelViewSet):  # Только GET
    queryset = AllProject.objects.all()
    serializer_class = AllProjectSerializer


# -------------------- Event -------------------- #
class EventViewSet(viewsets.ReadOnlyModelViewSet):  # Только GET
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# -------------------- Register -------------------- #
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Валидация
        if not PHONE_REGEX.match(instance.phone):
            raise serializers.ValidationError({'phone': 'Invalid phone number. Use +996XXXXXXXXX'})
        if instance.email and not EMAIL_REGEX.match(instance.email):
            raise serializers.ValidationError({'email': 'Invalid email format'})

        # Telegram
        message = (
            f"📞 Новая регистрация:\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Email: {instance.email or 'нет'}"
        )
        try:
            requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                          data={'chat_id': GROUP_ID, 'text': message}, timeout=5)
        except Exception as e:
            print(f"Telegram exception: {e}")





@api_view(['GET'])
def get_contacts(request):
    contact = Contact.objects.first()
    return Response(ContactSerializer(contact).data if contact else {})


class ContactViewSet(viewsets.ReadOnlyModelViewSet):  # Только GET
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer