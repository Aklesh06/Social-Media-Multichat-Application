from django import forms
from .models import Post,Comment,Event,EventComment

class ImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("caption", "image")
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'custom-caption-class','placeholder': 'Enter Caption for Post'}),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-image-class'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.caption = self.cleaned_data['caption']

        if commit:
            instance.save()

        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'custom-text-class','placeholder': 'Enter Your Comment'}),
        }
    

class EventImageForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("caption", "image")
        widgets = {
            '': forms.Textarea(attrs={'class': 'custom-Eventcaption-class','placeholder': 'Enter Caption for Event Post'}),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-Eventimage-class'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(EventImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.caption = self.cleaned_data['caption']

        if commit:
            instance.save()

        return instance

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'custom-Eventtext-class','placeholder': 'Enter Your Comment'}),
        }