from django.db import models
from django.utils.timesince import timesince
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class PeerkadaAccount(AbstractUser):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length= 100)
    username = models.CharField(max_length=100, unique = True)
    place = models.CharField(max_length=100)
    birthday = models.DateField(null = True)
    email = models.EmailField()
    
    sex_choices = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    sex = models.CharField(max_length=1, choices=sex_choices)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=50)
    is_counselor = models.BooleanField(default=False)
    avatar = models.ImageField(null=True)
    USERNAME_FIELD = 'username' 
    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return 'https://picsum.photos/200/200'

    


class Stats(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    created_by = models.ForeignKey(PeerkadaAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    
    OPTION_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    optimism = models.IntegerField(choices=OPTION_CHOICES)
    usefulness = models.IntegerField(choices=OPTION_CHOICES)
    relaxed = models.IntegerField(choices=OPTION_CHOICES)
    interest_in_others = models.IntegerField(choices=OPTION_CHOICES)
    energy_to_spare = models.IntegerField(choices=OPTION_CHOICES)
    deal_with_problems_well = models.IntegerField(choices=OPTION_CHOICES)
    clearliness = models.IntegerField(choices=OPTION_CHOICES)
    good_about_yourself = models.IntegerField(choices=OPTION_CHOICES)
    close_to_other_people = models.IntegerField(choices=OPTION_CHOICES)
    confident = models.IntegerField(choices=OPTION_CHOICES)
    make_up_your_own_mind_about_things = models.IntegerField(choices=OPTION_CHOICES)
    loved = models.IntegerField(choices=OPTION_CHOICES)
    interested_in_new_things = models.IntegerField(choices=OPTION_CHOICES)
    cheerfulness = models.IntegerField(choices=OPTION_CHOICES)
    
    

class Conversation(models.Model):
    id = models.CharField(max_length = 5 , primary_key=True)
    users =models.ManyToManyField(PeerkadaAccount, related_name='recieved_mesasages')
    created_at = models.DateTimeField(auto_now_add= True)
    modified_at =models.DateTimeField(auto_now_add= True)
    def modified_at_formatted(self):
       return timesince(self.created_at)

class ConversationMessages(models.Model):
    id = models.CharField(max_length = 5 , primary_key=True)
    sent_to = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    created_by =models.ForeignKey(PeerkadaAccount, related_name = 'sent_mesasages', on_delete=models.CASCADE)


class Notification(models.Model):
    id = models.CharField(max_length = 5, primary_key = True)
    user = models.ForeignKey(PeerkadaAccount, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def created_at_formatted(self):
       return timesince(self.created_at)

class Comment(models.Model):
    id=models.CharField(max_length = 5, primary_key = True)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(PeerkadaAccount, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    id=models.CharField(max_length = 5, primary_key = True)
    created_by = models.ForeignKey(PeerkadaAccount, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class EmotionsSharing(models.Model):
    id=models.CharField(max_length = 5, primary_key = True)
    body = models.TextField()
    comments = models.ManyToManyField(Comment, blank=True)
    like = models.ManyToManyField(Like, blank=True)
    created_by = models.ForeignKey(PeerkadaAccount, related_name = 'sharer', on_delete=models.CASCADE)

class Appointment(models.Model):
    id = models.CharField(max_length = 5, primary_key = True)
    description = models.TextField()
    counselor = models.ForeignKey(PeerkadaAccount, related_name = 'counselor_name', on_delete=models.CASCADE)
    created_by = models.ForeignKey(PeerkadaAccount, related_name = 'appointee', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_attended = models.BooleanField(default=False)

