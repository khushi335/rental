from django import forms
from .models import Property , ShiftHome, FindMeRoom, Inquiry, Review

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'category', 'price', 'location', 'available_date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Spacious 2BHK Apartment'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your property...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1200'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Area'}),
            'available_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FindMeRoomForm(forms.ModelForm):
    class Meta:
        model = FindMeRoom
        fields = ['full_name', 'email', 'phone', 'preferred_location', 'room_type', 'price_min', 'price_max', 'message', 'deposit_slip']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'deposit_slip': forms.FileInput(),
        }

class ShiftHomeForm(forms.ModelForm):
    class Meta:
        model = ShiftHome
        exclude = ['user', 'created_at', 'status']
        widgets = {
            'when': forms.RadioSelect(),
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'schedule_time': forms.TimeInput(attrs={'type': 'time'}),
            'deposit_slip': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deposit_slip'].required = True

    def clean(self):
        cleaned_data = super().clean()
        when = cleaned_data.get('when')
        schedule_date = cleaned_data.get('schedule_date')
        schedule_time = cleaned_data.get('schedule_time')

        # Conditional validation
        if when == 'Later':
            if not schedule_date:
                self.add_error('schedule_date', 'Schedule date is required for later booking.')
            if not schedule_time:
                self.add_error('schedule_time', 'Schedule time is required for later booking.')

        # Optional: Validate phone number format (very simple example)
        phone = cleaned_data.get('phone')
        if phone and not phone.isdigit():
            self.add_error('phone', 'Phone number must contain only digits.')

        return cleaned_data

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone', 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message...', 'rows': 6, 'required': True}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.Select(choices=[(i / 2, f"{i / 2} ⭐") for i in range(1, 11)])
        }