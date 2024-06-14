from django.contrib import admin


# Custom Admin Registration.
from core.models import Post, MidiFile, Chapter, Testimonial

class Table:
    def __init__(self, name, model, fields=None, order_by=None) -> None:
        self.name = name
        self.model = model
        self.fields = fields
        self.order_by = order_by

models = [
    Table(
        name="Post",
        model=Post,
        fields=["user", "title", "date_created"],
        order_by=["-date_created"]
    ),
        Table(
        name="MidiFile",
        model=MidiFile,
        fields=["user", "name", "genere", "key", "emotion"],
        order_by=["-date_created"]
    ),
    Table(
        name="Chapter",
        model=Chapter,
        fields=["title"],

    ),
    Table(
        name="Testimonial",
        model=Testimonial,
    ),
]