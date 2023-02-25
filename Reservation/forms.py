from django import forms
from django.utils import timezone
from Reservation.models import Reservations, Customer, Facility, Prices
from Home.models import Gallery
from Reservation.reservation_function.availability import check_availability

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = {"firstname", "lastname", "contactNumber", "email"}
        widgets = {
            "firstname": forms.TextInput(attrs={"class": "form-control"}),
            "lastname": forms.TextInput(attrs={"class": "form-control"}),
            "contactNumber": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "firstname": "First Name",
            "lastname": "Last Name",
            "contactNumber": "Contact Number",
            "email": "Email",
        }


class ReservationForm(forms.ModelForm):
    model = Reservations
    class Meta:
        model = Reservations
        fields = (
            "checkIn",
            "checkOut",
            "downpayment",
            "totalPayment",
            "balance",
            'prices',
            'facility',
        )
        widgets = {
            'checkIn' : forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'checkOut' : forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'totalPayment' : forms.TextInput(attrs={'class' : 'form-control', 'readonly':'True',}),
            'balance' : forms.TextInput(attrs={'class' : 'form-control', 'readonly':'True'}),
            'downpayment' : forms.TextInput(attrs={'class' : 'form-control', 'readonly':'True',}),
            'facility' : forms.CheckboxSelectMultiple(attrs={'class' : 'form-control'})
        }

        labels = {
            "checkIn": "Check In Date",
            "checkOut": "Check Out Date",
            "totalPayment": "Total",
            "downpayment": "Downpayment Required",
            "balance": "Payment Balance",
            'facility': 'Additional Facilities'
        }

    def clean(self):
        cleaned_data=super().clean()
        prices=cleaned_data.get("prices")
        checkIn = cleaned_data.get("checkIn")
        checkOut = cleaned_data.get("checkOut")
        if checkIn < timezone.now().date():
            raise forms.ValidationError("Check in date cannot be in the past")
        if checkOut < timezone.now().date():
            raise forms.ValidationError("Check Out date cannot be in the past")
        if checkOut < checkIn:
            raise forms.ValidationError("Check Out date cannot be earlier than check in")
        check1 = ''
        checkID=0
        data2=Prices.objects.all().values()
        for price in data2:
            check1 = 'For '+price['dayTime'] +' Reservation with Maximum of '+str(price['maxPax'])+ ' Pax'
            if check1 == str(prices):
                checkID=price['id']
        prices_list = Prices.objects.filter(id = checkID).values_list('id')
        available_price=[]
        for price in prices_list:
            print(check_availability(price, checkIn,checkOut))
            if check_availability(price, checkIn,checkOut):
                available_price.append(price)
        if len(available_price)>0:
            av_price = available_price[0] 
            print('Available')
        else:
            print('no room available')
            raise forms.ValidationError("Date not available") 
        print(prices) 
        return cleaned_data
    


class FacilityForm(forms.ModelForm):
    model = Facility
    class Meta:
        model = Facility
        FacilityCategoriesChoices = (
            ('pool','Pool'),
            ('rooms','Rooms'),
            ('cottages','Cottages'),
            ('EH','Event Hall'),
     
  )
        fields = ( 'facilityName', 'facilityDescription', 'facilityPic', 'facilityPrice','facilityCategory', 'facilitymax')
        widgets = {
            'facilityName' : forms.TextInput(attrs={'class': 'form-control'}),
            'facilityDescription' : forms.Textarea(attrs={'class': 'form-control'}),
            
            'facilityPrice' : forms.NumberInput(attrs={'class': 'form-control'}),
            'facilitymax' : forms.NumberInput(attrs={'class': 'form-control'}),
            
            'facilityCategory': forms.RadioSelect(choices=FacilityCategoriesChoices),
        }
        labels = {
            'facilityName' : 'Facility Name',
            'facilityDescription' : 'Facility Description',
            'facilityPic' : 'Facility Pic',
            'facilityPrice' : 'Facility Price',
            'facilitymax' : 'Facility Maximum Occupancy',
            'facilityCategory' : 'Category'
            
        }

class PriceForm(forms.ModelForm):
    model = Prices
    class Meta:
        model = Prices
        dayTimeChoices = (
            ('day','Day'),
            ('night','Night'),
            ('whole','Whole Day')
        )

        maxPaxChoices = (
            (30, '30 pax'),
            (50, '50 pax'),
            (100, '100 pax'),
            (150, '150 pax')
        )
        fields = ('price', 'maxPax', 'dayTime')
        widgets = {

            'price' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'maxPax': forms.RadioSelect(choices=maxPaxChoices, attrs={'class' : 'form-control'}),
            'dayTime': forms.RadioSelect(choices=dayTimeChoices, attrs={'class' : 'form-control'})
        }

        label = {
            'price': 'Price',
            'dayTime' : 'Schedule',
            'maxPax' : 'Maximum Guest'
        }


