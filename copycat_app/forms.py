from django import forms
from django.core.exceptions import ValidationError
from copycat_app.models import Profile, User, Tag, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", min_length=4, max_length=36, widget=forms.TextInput)
    password = forms.CharField(label="Password", min_length=8, max_length=64, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", min_length=4, max_length=36, widget=forms.TextInput)
    email = forms.CharField(label="Email", min_length=4, widget=forms.EmailInput)
    display_name = forms.CharField(label="Display name", min_length=4, max_length=36, widget=forms.TextInput)
    password = forms.CharField(label="Password", min_length=8, max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Password confirmation", min_length=4,
                                       max_length=64, widget=forms.PasswordInput)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).first():
            raise ValidationError("This username is already taken.")
        return self.cleaned_data['username']

    def clean_display_name(self):
        if Profile.objects.filter(display_name=self.cleaned_data['display_name']).first():
            raise ValidationError("This display name is already taken.")
        return self.cleaned_data['display_name']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    def save(self):
        name = self.cleaned_data.pop("display_name")
        self.cleaned_data.pop("confirm_password")
        new_user = User.objects.create_user(**self.cleaned_data)
        new_profile = Profile.objects.create(display_name=name, user=new_user)
        new_profile.save()
        return new_user


class QuestionForm(forms.Form):
    title = forms.CharField(label="Title:", min_length=4, max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="Content:", min_length=4, max_length=1000,
                              widget=forms.Textarea(attrs={'placeholder': 'Enter your question here...'}))
    tags = forms.CharField(label="Tags:", max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'python technopark ...'}))

    def clean_tags(self):
        tags = [tag.strip() for tag in self.cleaned_data['tags'].lower().split()]
        for tag in tags:
            if not 3 <= len(tag) <= 12:
                raise ValidationError("Tag length must be 3 to 12 symbols.")
        return tags

    def save(self, author):

        tags = self.cleaned_data.pop('tags')
        print(self.cleaned_data)
        question_tags = []
        for tag in tags:
            existing_tag = Tag.objects.filter(text=tag).first()
            if existing_tag:
                existing_tag.uses += 1
            else:
                existing_tag = Tag.objects.create(text=tag, uses=1)
                existing_tag.save()
            question_tags.append(existing_tag)

        question = Question.objects.create(author=author, **self.cleaned_data)
        question.tags.set(question_tags)
        question.save()
        return question


class AnswerForm(forms.Form):
    content = forms.CharField(label="Your answer:", min_length=4, max_length=1000,
                              widget=forms.Textarea(attrs={'placeholder': 'Enter your answer here...',
                                                           'rows': 3}))

    def save(self, author, question):
        answer = Answer.objects.create(question=question, author=author, **self.cleaned_data)
        answer.save()
        return answer


class ProfileForm(forms.Form):
    email = forms.CharField(required=False, label="Email:", max_length=32,
                            widget=forms.TextInput(attrs={'placeholder': 'Enter new email'}))
    display_name = forms.CharField(required=False, label="Display name:", max_length=32,
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter new display name'}))
    profile_picture = forms.ImageField(required=False, label="New profile picture:")

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')
        if display_name:
            if Profile.objects.filter(display_name=display_name).first():
                raise ValidationError("This display name is taken")
            else:
                return display_name

    def save(self, user):
        print(self.cleaned_data)
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        if self.cleaned_data.get('display_name'):
            user.profile.display_name = self.cleaned_data['display_name']
        if self.cleaned_data.get('profile_picture'):
            user.profile.profile_picture = self.cleaned_data['profile_picture']
        user.save()
        user.profile.save()

