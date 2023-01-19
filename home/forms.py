from django import forms
from .models import *
class ColaForm(forms.ModelForm):
    class Meta:
        model = ColaModel
        fields = '__all__'
        widgets ={
            'nombre_de_la_cola':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre de la Cola',
                'autocomplete':'off'
            }),
            'creada_por':forms.Select(attrs={
                'disabled':'disabled',
                'class':'form-control'
            }),
            'usuarios_acceso':forms.SelectMultiple(attrs={
                'class':'form-control'
            })
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = ColaItem
        fields = '__all__'
        widgets = {
            'cola':forms.Select(attrs={
                'disabled': 'disabled',
                'class': 'form-control'
            })
        }
