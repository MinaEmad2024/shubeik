from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings




# Create your models here.

# create customer profile
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     date_modified = models.DateTimeField(User, auto_now=True)
     phone = models.CharField(max_length=20)
     address1 = models.CharField(max_length=200, blank=True)
     address2 = models.CharField(max_length=200, blank=True)
     city = models.CharField(max_length=200, blank=True)
     state = models.CharField(max_length=200, blank=True)
     zipcode = models.CharField(max_length=200, blank=True)
     country = models.CharField(max_length=200, blank=True)
     old_cart = models.CharField(max_length=200, blank=True, null=True)


     def  __str__(self):
          return self.user.username

#create a user profile by default when A user sign up
def create_profile(sender, instance, created, **kwargs):
     if created:
          user_profile = Profile(user=instance)
          user_profile.save()

post_save.connect(create_profile, sender=User)     


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'      


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
            return f'{self.first_name} { self.last_name}'


GOVERNRATES = [
     ("1", "Qena"),
     ("2", "Sohag"),
     ("3", "Cairo")
]

Vendor_Category = [
     ("متنوع", "متنوع"),
     ("اكسسوارات", "اكسسوارات"),
     ("مطاعم", "مطاعم"),
     ("صيدليات", "صيدليات"),   
     ("ملابس", "ملابس"),
]

class Vendor(models.Model):
     name = models.CharField(max_length=100, default='', blank=False, null=False )
     image = models.ImageField(upload_to='uploads/product/')
     owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)
     address = models.CharField(max_length=500, default='', blank=False, null=False)
     governrate = models.CharField(max_length=50, choices=GOVERNRATES, default='', blank=False, null=False)
     open_at = models.TimeField(blank=False, null=False)
     close_at= models.TimeField(blank=False, null=False)
     phone = models.CharField(max_length=20, default='', blank=False, null=False)
     watts_app = models.CharField(max_length=20, default='', blank=False, null=False)
     email = models.EmailField(max_length=100)
     active_status = models.BooleanField(default=True)
     category = models.CharField(max_length=50, choices=Vendor_Category, default='', blank=False, null=False)

     def  __str__(self):
        return self.name
     
     def is_open(self, current_time):
        """Check if the place is open at a given time."""
        return self.open_at <= current_time <= self.close_at
       


class Product(models.Model):
     name = models.CharField(max_length=100)
     price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
     category = models.ForeignKey(Category ,on_delete=models.CASCADE )
     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
     description = models.CharField(max_length=250, default='', blank=True, null=True)
     image = models.ImageField(upload_to='uploads/product/')
     is_sale = models.BooleanField(default=False)
     sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
     is_not_available = models.BooleanField(default=False)

     def __str__(self):
          return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)



    def __str__(self):
        return self.product



class Review(models.Model):
    post = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    rating =  models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Review {} by {}'.format(self.body, self.name)