from django import forms

class UploadFileForm(forms.Form):
    archivo_excel = forms.FileField(label='Seleccionar archivo Excel', help_text='Solo se permiten archivos en formato .xlsx y .xls')
