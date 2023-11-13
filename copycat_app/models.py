from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from copycat.settings import os, Path, FAST_SIDE_BLOCK
from datetime import date, timedelta
from django.utils import timezone

# Create your models here.
BASE_DIR = Path(__file__).resolve().parent.parent


class ProfileManager(models.Manager):
    def top_last_week(self):
        questions = Question.objects.filter(date_submitted__range=[timezone.now() - timedelta(days=7),
                                                                   timezone.now()]).order_by('-rating')
        answers = Answer.objects.filter(date_submitted__range=[timezone.now() - timedelta(days=7),
                                                               timezone.now()]).order_by('-rating')
        if FAST_SIDE_BLOCK:
            profiles = []
            profiles.extend([question.author for question in questions[:5]])
            profiles.extend([answer.author for answer in answers[:6]])
            return profiles
        profiles = {}
        for question in questions:
            if not profiles.get(question.author):
                profiles[question.author] = question.rating
            else:
                profiles[question.author] += question.rating
        for answer in answers:
            if not profiles.get(answer.author):
                profiles[answer.author] = answer.rating
            else:
                profiles[answer.author] += answer.rating
        profiles = [profile for profile in sorted(profiles, key=profiles.get, reverse=True)][:10]
        return profiles


class TagManager(models.Manager):
    def top_last_week(self):
        questions = Question.objects.filter(date_submitted__range=[timezone.now() - timedelta(days=7),
                                                                   timezone.now()]).order_by('-rating')
        if FAST_SIDE_BLOCK:
            tags = [tag for tag in Tag.objects.order_by('-uses')[:10]]
            return tags
        tags = {}
        for question in questions:
            for tag in question.tags.all():
                if not tags.get(tag):
                    tags[tag] = 1
                else:
                    tags[tag] += 1
        tags = [tag for tag in sorted(tags, key=tags.get, reverse=True)][:10]
        return tags


class QuestionManager(models.Manager):
    def have_tags(self, tags):
        return Question.objects.filter(tags__text__in=tags).distinct().order_by('-date_submitted')

    def hot(self):
        return Question.objects.filter(date_submitted__range=[timezone.now() - timedelta(days=7),
                                                              timezone.now()]).order_by('-rating')

    def default(self):
        return Question.objects.order_by('-date_submitted')

    def specific(self, id_):
        return Question.objects.filter(id=id_).first()


class AnswerManager(models.Manager):
    def useful(self, question):
        return question.answers.order_by('-rating')


class Profile(models.Model):
    display_name = models.CharField(max_length=16, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures',
                                        default=os.path.join(BASE_DIR, 'static/img/pfp-default.png'))
    rating = models.BigIntegerField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    objects = ProfileManager()


class Tag(models.Model):
    text = models.CharField(max_length=12, null=True)
    uses = models.BigIntegerField(default=0)

    objects = TagManager()


class Question(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=1000, null=True)
    rating = models.BigIntegerField(null=True)
    date_submitted = models.DateTimeField(auto_now=True, null=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()


class Answer(models.Model):
    content = models.CharField(max_length=500, null=True)
    is_correct = models.BooleanField(default=False)
    rating = models.BigIntegerField(null=True)
    date_submitted = models.DateTimeField(auto_now=True, null=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='answers')

    objects = AnswerManager()


class QuestionRating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.BooleanField(null=True)  # 0 - negative; 1 - positive

    class Meta:
        unique_together = ['user', 'question']


class AnswerRating(models.Model):
    answer = models.ForeignKey(Question, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.BooleanField(null=True)  # 0 - negative; 1 - positive

    class Meta:
        unique_together = ['user', 'answer']



