from django import forms

from core.models import *

class FormImmobili(forms.ModelForm):
    fascia_prezzo = forms.ModelChoiceField(queryset=FasciaPrezzo.objects.all(), initial='', widget=forms.Select( attrs={'class': 'form-control'} ), required=False)
    contratto = forms.ModelChoiceField(queryset=Contratto.objects.all().order_by('pk'), initial='', widget=forms.Select( attrs={'class': 'form-control'} ), required=False)
    indirizzo = forms.CharField(required=True),
    stato = forms.CharField(required=False),
    citta = forms.CharField(required=False),
    prezzo = forms.CharField(required=False),
    zona = forms.CharField(required=False),
    immobili_proposti = forms.CharField(required=False),
    tipologia = forms.CharField(required=False),
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Immobile
        fields = ['indirizzo','stato','citta','prezzo','zona','immobili_proposti','mutuo','tipologia','contratto','cliente','note','fascia_prezzo']
        widgets = {
            'indirizzo': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'stato': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'citta':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'prezzo': forms.NumberInput(attrs={'placeholder':'','class':'form-control'}),
            'zona':forms.Textarea(attrs={'class':'form-control'}),
            'immobili_proposti':forms.Textarea(attrs={'class':'form-control'}),
            'tipologia':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'note':forms.Textarea(attrs={'class':'form-control'}),
            'cliente': forms.TextInput(attrs={'type':'hidden'}),
            'mutuo': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
        }

class FormFascia(forms.ModelForm):
    class Meta:
        model = FasciaPrezzo
        fields = ['fascia_min', 'fascia_max']
        widgets = {
            'fascia_min': forms.NumberInput(attrs={'class':'form-control'}),
            'fascia_max': forms.NumberInput(attrs={'class':'form-control'})
        }

class FormCliente(forms.ModelForm):
    inizio_incarico = forms.DateField(input_formats=['%Y-%m-%d'])
    fine_incarico = forms.DateField(input_formats=['%Y-%m-%d'])
    scadenza = forms.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Cliente
        fields = ['nome','cognome','email','citta','telefono_fisso','telefono_cellulare','cliente','inizio_incarico','fine_incarico','scadenza']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'cognome':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'email':forms.EmailInput(attrs={'placeholder': '','class':'form-control'}),
            'citta':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'telefono_cellulare':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'telefono_fisso':forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'cliente': forms.TextInput(attrs={'placeholder': '','class':'form-control'}),
            'inizio_incarico': forms.DateInput(attrs={'class':'form-control'}),
            'fine_incarico': forms.DateInput(attrs={'class':'form-control'}),
            'scadenza': forms.DateInput(attrs={'class':'form-control'}),
        }

