from django.db import models

class Post(models.Model):
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    init_message = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

class Message(models.Model):
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)
    post = models.ForeignKey("core.Post", on_delete=models.CASCADE, )
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} : {self.content}"
    

class MidiFile(models.Model):
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE)
    file = models.FileField(upload_to="midi_files/", max_length=100)
    name = models.CharField(max_length=100)
    genere = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    emotion = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)
    

class Chapter(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    rank = models.IntegerField()


    def __str__(self):
        return self.title
    

class Testimonial(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField()
    full_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.full_name


class Support_message(models.Model):
    user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE, related_name="support_message_as_user")
    sender = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE, related_name="support_message_as_sender")
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.sender}"
