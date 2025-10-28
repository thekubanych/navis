from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from ckeditor.fields import RichTextField

class Post(models.Model):
    img = models.FileField(upload_to='files/')
    title = models.CharField(max_length=200)
    description = models.TextField()
    ckeditor = RichTextField()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

# vakansiya
class Vacancy(models.Model):
    level_choises = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=level_choises)
    salary_som = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    requirements = RichTextField(blank=True, null=True, help_text="Требования к кандидату")
    responsibilities = RichTextField(blank=True, null=True, help_text="Обязанности кандидата")
    conditions = RichTextField(blank=True, null=True, help_text="Условия работы")

    class Meta:
        verbose_name = 'vsksnsi'
        verbose_name_plural = 'vakansi'

    def __str__(self):
        return self.title

# zayavka
class Application(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = RichTextField(blank=True, null=True, help_text="kommentarii kondidata")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')


    class Meta:
        verbose_name = 'zayavka na vakansi'
        verbose_name_plural = 'zayavka na vakansi'

    def __str__(self):
        return f"{self.name} - {self.vacancy.title}"



# o nas ,instrumenty ,kontakty
class WeSelf(models.Model):
    img = models.FileField(upload_to='files/')
    title = models.CharField(max_length=200, default="О нас")
    description = RichTextField(help_text="about company, selyah i komande")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255, blank=True, null=True)
    tools = models.CharField(max_length=300, default="Python, Django, Java, HTML, CSS, JavaScript, PostgreSQL",help_text="Инструменты , kotorie vy ispolzuete"
    )
    github_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def __str__(self):
        return self.title

# free consultation
class FreeConsultation(models.Model):
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=255,blank=True,null=True)
    house_working = models.CharField(max_length=200,
                                     default="Пн–Пт: 9:00–18:00, Сб–Вс: выходной",
                                     help_text='rejim kompany raboty')



    class Meta:
        verbose_name = 'rejim raboty'
        verbose_name_plural = 'rejim raboty'

    def __str__(self):
        return self.name
# http://127.0.0.1:8000/api/free-consultation/ {
#     "name": "Кубаныч",
#     "phone": "+996500000000",
#     "email": "test@mail.com",
#     "address": "Бишкек, пр. Чуй 120",
#     "house_working": "Пн–Пт: 10:00–17:00"
# }

# str
#
#
# kagdogo napravleniya
class DesignPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="zagolovok stranitsa")
    description = RichTextUploadingField(verbose_name="osnovnoe opisanie")

    # bloki kontenta
    section1_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="zagalovka blok 1")
    section1_content = RichTextUploadingField(blank=True, null=True, verbose_name="kontent bloka 1")

    section2_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="zagalovka blok 2")
    section2_content = RichTextUploadingField(blank=True, null=True, verbose_name="kontent bloka 2")

    section3_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="zagalovka blok  3")
    section3_content = RichTextUploadingField(blank=True, null=True, verbose_name="kontent bloka 3")

    section4_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="zagalovka blok 4")
    section4_content = RichTextUploadingField(blank=True, null=True, verbose_name="kontent bloka 4")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "stranitsa UX/UI dizayn"
        verbose_name_plural = "stranitsa UX/UI dizayn"

    def __str__(self):
        return self.title


class AllProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)



    class Meta:
        verbose_name = 'все проекты'
        verbose_name_plural = 'все проекты'

    def __str__(self):
        return self.title


# meropriyatiya

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = RichTextUploadingField(verbose_name="Описание")
    requirements = RichTextUploadingField(blank=True, verbose_name="Требования")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-date']

    def __str__(self):
        return self.title

