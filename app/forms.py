from django import forms
from app.fields import ListTextWidget


class FormForm(forms.Form):
    char_field_with_list = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        _city_list = kwargs['datalist']
        super(FormForm, self).__init__()

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['char_field_with_list'].widget = ListTextWidget(datalist=_city_list, name='city-list')
        self.fields['char_field_with_list'].widget.attrs.update({'class': 'form-control bg-dark text-white'})
        self.fields['char_field_with_list'].widget.attrs.update({'name': 'local'})
        self.fields['char_field_with_list'].widget.attrs.update({'placeholder': 'Procurar localização...'})