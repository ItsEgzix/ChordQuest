from django import forms
from .models import Post, MidiFile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "init_message"]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': '', 'placeholder': 'Title'}),
            'init_message': forms.Textarea(attrs={'class': '', 'placeholder': 'Enter a message...', 'rows': '3'}),

        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Add custome css class to all input widgets.
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class') or ''
            field.widget.attrs['class'] = current_class+" "+'forum-input'

class MidiFileForm(forms.ModelForm):
    class Meta:
        model = MidiFile
        fields = ["file", "name", "genere", "key", "emotion"]
        widgets = {
            'name': forms.TextInput(attrs={'class': '', 'placeholder': 'Name'}),
            'genere': forms.TextInput(attrs={'class': '', 'placeholder': 'Genere'}),
            'key': forms.TextInput(attrs={'class': '', 'placeholder': 'Key'}),
            'emotion': forms.TextInput(attrs={'class': '', 'placeholder': 'Emotion'}),

        }
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Add custome css class to all input widgets.
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class') or ''
            field.widget.attrs['class'] = current_class+" "+'regular-input'
