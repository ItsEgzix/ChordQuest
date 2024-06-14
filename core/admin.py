from django.contrib import admin
from .models import Post, Message, MidiFile, Chapter, Testimonial

admin.site.register(Post)
admin.site.register(Message)
admin.site.register(MidiFile)
admin.site.register(Chapter)
admin.site.register(Testimonial)