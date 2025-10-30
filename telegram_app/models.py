from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Post
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


# Vacancy
class Vacancy(models.Model):
    LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    salary_som = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    requirements = RichTextField(blank=True, null=True)
    responsibilities = RichTextField(blank=True, null=True)
    conditions = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = 'vacancy'
        verbose_name_plural = 'vacancies'

    def __str__(self):
        return self.title


# Application
class Application(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    comment = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')

    class Meta:
        verbose_name = 'application'
        verbose_name_plural = 'applications'

    def __str__(self):
        return f"{self.name} - {self.vacancy.title}"


# WeSelf
class WeSelf(models.Model):
    img = models.FileField(upload_to='files/')
    title = models.CharField(max_length=200, default="О нас")
    description = RichTextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255, blank=True, null=True)
    tools = models.CharField(max_length=300, default="Python, Django, Java, HTML, CSS, JavaScript, PostgreSQL")
    github_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'WeSelf'
        verbose_name_plural = 'WeSelf'

    def __str__(self):
        return self.title


# FreeConsultation
class FreeConsultation(models.Model):
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)
    house_working = models.CharField(max_length=200, default="Пн–Пт: 9:00–18:00, Сб–Вс: выходной")

    class Meta:
        verbose_name = 'Free Consultation'
        verbose_name_plural = 'Free Consultations'

    def __str__(self):
        return self.name


# DesignPage
class DesignPage(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    section1_title = models.CharField(max_length=255, blank=True, null=True)
    section1_content = RichTextUploadingField(blank=True, null=True)
    section2_title = models.CharField(max_length=255, blank=True, null=True)
    section2_content = RichTextUploadingField(blank=True, null=True)
    section3_title = models.CharField(max_length=255, blank=True, null=True)
    section3_content = RichTextUploadingField(blank=True, null=True)
    section4_title = models.CharField(max_length=255, blank=True, null=True)
    section4_content = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Design Page'
        verbose_name_plural = 'Design Pages'

    def __str__(self):
        return self.title


# AllProject
class AllProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


# Event
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    requirements = RichTextUploadingField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-date']

    def __str__(self):
        return self.title


# Register
class Register(models.Model):
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Register'
        verbose_name_plural = 'Register'

    def __str__(self):
        return self.username

