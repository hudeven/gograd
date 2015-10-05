from django import forms

from .models import Post, Comment 

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

POSITION_CHOICES = (
    ('asp', 'assistant professor'),
    ('ap', 'associate professor'), 
    ('postdoc', 'Post-Doctoral Fellow'), 
    ('tp', 'Teaching Professor'), 
)

class SearchForm(forms.Form):
    position = forms.ChoiceField(choices=POSITION_CHOICES)
      

