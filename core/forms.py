from django import forms
from .models import PointVente
from django.utils.translation import gettext_lazy as _

class PointVenteForm(forms.ModelForm):
    class Meta:
        model = PointVente
        fields = ['nom', 'commune', 'latitude', 'longitude', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'commune': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ex: 18.070000'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ex: -15.950000'
            }),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'latitude': 'Entrez la latitude (ex: 18.079033)',
            'longitude': 'Entrez la longitude (ex: -15.965276)',
        }

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        # Vérifier que les coordonnées sont dans des plages valides
        if latitude and (latitude < -90 or latitude > 90):
            self.add_error('latitude', 'La latitude doit être entre -90 et 90 degrés')
        
        if longitude and (longitude < -180 or longitude > 180):
            self.add_error('longitude', 'La longitude doit être entre -180 et 180 degrés')

        return cleaned_data
