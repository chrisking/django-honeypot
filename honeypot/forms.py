from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Name*")
    company = forms.CharField(label="Company*")
    email = forms.EmailField(label="Email*")
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zipcode = forms.CharField(required=False)
    country = forms.CharField(required=False)
    telephone = forms.CharField(required=False)
    fax = forms.CharField(required=False)

    def getEmailBody(self):
        body = 'Name: ' + self.cleaned_data['name']
        body += '\n Company: ' + self.cleaned_data['company']
        body += '\n Address: ' + self.cleaned_data['address']
        body += '\n Email: ' + self.cleaned_data['email']
        body += '\n City: ' + self.cleaned_data['city']
        body += '\n State: ' + self.cleaned_data['state']
        body += '\n Zipcode: ' + self.cleaned_data['zipcode']
        body += '\n Country: ' + self.cleaned_data['country']
        body += '\n Telephone: ' + self.cleaned_data['telephone']
        body += '\n Fax: ' + self.cleaned_data['fax']
        return body

    def clean_address(self):
        data = self.cleaned_data['address']
        if "http://" in data:
            raise forms.ValidationError("SPAMBOT")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

class QuoteForm(ContactForm):
    part_numbers= forms.CharField(required=False, label="Part Numbers", widget=forms.Textarea())

    def getEmailBody(self):
        body = ContactForm.getEmailBody(self)
        body += '\n Part Numbers: ' + self.cleaned_data['part_numbers']



class SellForm(ContactForm):
    partsDescription = forms.CharField(widget=forms.Textarea(), label='Part Numbers , Quantity & New-Sealed or Used: *')

    def getEmailBody(self):
        body = ContactForm.getEmailBody(self)
        body += '\n Part Numbers: ' + self.cleaned_data['partsDescription']
        return body