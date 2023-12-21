from django.core.management.base import BaseCommand
from copycat_app.models import User, Profile, Question, Answer, Tag
from faker import Faker
from random import choice, randrange, choices
from uuid import uuid4
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import date, timedelta
from tqdm import tqdm

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with users, questions, and answers..."

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs["ratio"]
        print(f"STARTING DB FILL-UP - ratio:{ratio}")
        users = [
            User(
                username=uuid4().hex,
                password=make_password(fake.slug()),
                email=fake.safe_email()
            ) for _ in tqdm(range(ratio))
        ]
        if not User.objects.filter(username="admin").first():
            users.append(
                User(
                    username="admin",
                    password=make_password("insecurepassword"),
                    is_superuser=True,
                    is_staff=True,
                    is_active=True
                )
            )
        User.objects.bulk_create(users)
        print("FINISHED USER CREATION")
        users = User.objects.all()
        profiles = [
            Profile(
                user=user,
                display_name=fake.user_name()[:10] + uuid4().hex[:6],
                rating=0,
                profile_picture=f'profile_pictures/{randrange(1,10)}.jpeg'
            ) for user in tqdm(users)
        ]
        Profile.objects.bulk_create(profiles)
        print("FINISHED PROFILE CREATION")
        profiles = Profile.objects.all()
        tags = [
            Tag(
                text=fake.sentence(nb_words=1)[:12][:-1].lower(),
                uses=randrange(1, ratio * 10)
            ) for _ in tqdm(range(ratio))
        ]
        Tag.objects.bulk_create(tags)
        print("FINISHED TAG CREATION")
        tags = Tag.objects.all()
        questions = [
            Question(
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=9),
                rating=0,
                author=choice(profiles),
            ) for _ in tqdm(range(ratio * 10))
        ]
        Question.objects.bulk_create(questions)
        print("FINISHED QUESTION CREATION")
        questions = Question.objects.all()
        for question in questions:
            tags_ = choices(tags, k=4)
            question.tags.set(tags_)
        answers = [
            Answer(
                content=fake.paragraph(nb_sentences=5),
                rating=0,
                author=choice(profiles),
                question=choice(questions)
            ) for _ in tqdm(range(ratio * 100))
        ]
        Answer.objects.bulk_create(answers)
        print("FINISHED ANSWER CREATION")
        answers = Answer.objects.all()

