from django import forms
from .models import Post, Comment

class PostupdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body')

class CommentcreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets={
            'body': forms.Textarea(attrs={'class':'form-control'})
        }

class ReplycreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }