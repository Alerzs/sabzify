import re

from django import forms

from .models import ServiceRequest

FIELD = (
    'w-full rounded-xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm text-neutral-900 '
    'outline-none transition placeholder:text-neutral-400 focus:border-sabz focus:bg-white '
    'focus:ring-4 focus:ring-sabz/10'
)


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            'full_name',
            'phone',
            'email',
            'city',
            'address',
            'service',
            'area',
            'preferred_date',
            'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': FIELD, 'placeholder': 'مثلاً علی رضایی'}),
            'phone': forms.TextInput(attrs={'class': FIELD, 'placeholder': '۰۹۱۲۱۲۳۴۵۶۷', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'class': FIELD, 'placeholder': 'name@email.com'}),
            'city': forms.TextInput(attrs={'class': FIELD, 'placeholder': 'تهران'}),
            'address': forms.Textarea(attrs={'class': FIELD, 'rows': 3, 'placeholder': 'محله، خیابان، پلاک'}),
            'service': forms.Select(attrs={'class': FIELD}),
            'area': forms.TextInput(attrs={'class': FIELD, 'placeholder': 'مثلاً ۸۰ متر'}),
            'preferred_date': forms.DateInput(attrs={'class': FIELD, 'type': 'date'}),
            'message': forms.Textarea(attrs={'class': FIELD, 'rows': 4, 'placeholder': 'وضعیت فعلی باغ یا حیاط را کوتاه بنویسید'}),
        }
        error_messages = {
            'full_name': {'required': 'لطفاً نام و نام خانوادگی را وارد کنید.'},
            'phone': {'required': 'لطفاً شماره تماس را وارد کنید.'},
            'city': {'required': 'لطفاً شهر را وارد کنید.'},
            'address': {'required': 'لطفاً آدرس را وارد کنید.'},
            'service': {'required': 'لطفاً نوع خدمت را انتخاب کنید.'},
            'email': {'invalid': 'ایمیل واردشده معتبر نیست.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['area'].required = False
        self.fields['preferred_date'].required = False
        self.fields['message'].required = False
        self.fields['city'].required = True
        self.fields['address'].required = True
        self.fields['service'].choices = ServiceRequest.SERVICE_CHOICES

    def clean_full_name(self):
        name = ' '.join(self.cleaned_data['full_name'].split())
        if len(name) < 3:
            raise forms.ValidationError('نام باید حداقل سه حرف باشد.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10 or len(digits) > 13:
            raise forms.ValidationError('یک شماره تماس معتبر وارد کنید.')
        return phone


class ContactForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['full_name', 'phone', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': FIELD, 'placeholder': 'نام شما'}),
            'phone': forms.TextInput(attrs={'class': FIELD, 'placeholder': 'شماره تماس', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'class': FIELD, 'placeholder': 'ایمیل (اختیاری)'}),
            'message': forms.Textarea(attrs={'class': FIELD, 'rows': 4, 'placeholder': 'پیام شما'}),
        }
        error_messages = {
            'full_name': {'required': 'لطفاً نام خود را بنویسید.'},
            'phone': {'required': 'لطفاً شماره تماس را وارد کنید.'},
            'message': {'required': 'لطفاً پیام خود را بنویسید.'},
            'email': {'invalid': 'ایمیل واردشده معتبر نیست.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['message'].required = True

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10 or len(digits) > 13:
            raise forms.ValidationError('یک شماره تماس معتبر وارد کنید.')
        return phone

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.service = 'consult'
        obj.city = 'تهران'
        obj.address = 'ثبت‌شده از صفحه تماس'
        if commit:
            obj.save()
        return obj
