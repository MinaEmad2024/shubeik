from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile, Category, Vendor, Product, GOVERNRATES, Vendor_Category


class UserInfoForm(forms.ModelForm):
		phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
		address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=False)
		address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
		city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
		state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
		zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
		country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

		class Meta:
			model = Profile
			fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )


	

class ChangePasswordForm(SetPasswordForm):
	class Meta :
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UpdateUserForm(UserChangeForm):
	# hide password stuff
	password = None
	# get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'




class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class CategoryForm(forms.ModelForm):
	name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add category'}), required=True)

	class Meta:
		model = Category
		fields = ['name', ] 



class VendorForm(forms.ModelForm):

	name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' Enter shop Name'}), required=True , error_messages = {'required':"Please Enter your Name1"})
	image = forms.ImageField(label="upload shop image", required=False , error_messages = {'required':"Please Enter your Name2"})
	# owner = forms.IntegerField(widget=forms.HiddenInput(), required=True, error_messages = {'required':"Please Enter your Name10"})
	# owner = forms.ModelChoiceField(label="",queryset= User.objects.filter(id=request.user.id), widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''}), required=True)
	address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add shop address'}), required=True,  error_messages = {'required':"Please Enter your Name3"})
	governrate = forms.ChoiceField(label="Choose your Governrate", required=True, choices=GOVERNRATES, error_messages = {'required':"Please Enter your Name4"})
	open_at = forms.TimeField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add open time'}), required=True, error_messages = {'required':"Please Enter your Name5"})
	close_at = forms.TimeField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add close time'}), required=True, error_messages = {'required':"Please Enter your Name6"})
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add phone'}), required=True, error_messages = {'required':"Please Enter your Name7"})
	watts_app = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add wattsapp'}), required=True, error_messages = {'required':"Please Enter your Name8"})
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' add email'}), required=True, error_messages = {'required':"Please Enter your Name9"})
	category = forms.ChoiceField(label="Choose a Category", required=True, choices=Vendor_Category, error_messages = {'required':"Please Enter your Name10"})

	def __init__(self, *args, **kwargs):
			self.request = kwargs.pop("request")
			super(VendorForm, self).__init__(*args, **kwargs)
			# self.fields["owner"].queryset = Profile.objects.filter(user=self.request.user)

	# def __init__(self, *args, **kwargs):
	# 				user = kwargs.pop('user', None)
	# 				super().__init__(*args, **kwargs)
	# 				if user:
	# 					self.fields['owner'].initial = user



	class Meta:
		model = Vendor
		fields= ('name', 'image', 'address', 'governrate', 'open_at', 'close_at', 'phone', 'watts_app', 'email', 'category')


class Product_Form(forms.ModelForm):
	name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' enter your product name'}), required=True , error_messages = {'required':"Please Enter your Name1"})
	price = forms.DecimalField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' price'}), required=True , error_messages = {'required':"Please Enter your Name2"})
	category = forms.ModelChoiceField(label="category",queryset=Category.objects.all() , required=True,  error_messages = {'required':"Please Enter your Name3"})
	# vendor = forms.CharField(label="vendor", widget=forms.Select(attrs={'class':'form-control', 'disabled': 'disabled'}), required=False)
	description = forms.CharField(label="description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' description'}), required=True , error_messages = {'required':"Please Enter your Name4"})
	image = forms.ImageField(label="upload product image", required=False,  error_messages = {'required':"Please Enter your Name5"})
	is_sale = forms.BooleanField(label="is_sale", required=False , error_messages = {'required':"Please Enter your Name6"})
	sale_price = forms.DecimalField(label="sale_price", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':' sale price'}), required=True , error_messages = {'required':"Please Enter your Name7"})
	is_not_available = forms.BooleanField(label="is_not_available", required=False , error_messages = {'required':"Please Enter your Name8"})

	def __init__(self, *args, **kwargs):
			self.request = kwargs.pop("request")
			super(Product_Form, self).__init__(*args, **kwargs)
			# owner = Profile.objects.get(user=self.request.user)
			# self.fields["vendor"].queryset = Vendor.objects.filter(owner = owner)

	class Meta:
		model = Product
		fields = ("name", "price", "category", "description", "image", "is_sale", "sale_price", "is_not_available")