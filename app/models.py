from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
# Create your models here.

# customer model
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),
                ("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Delhi","Delhi"),("Goa","Goa"),("Gujarat","Gujarat"),
                ("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
                ("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),
                ("Madhya Pradesh","Madhya Pradesh"),
                ("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),
                ("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),
                ("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),
                ("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
                ("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),
                ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),
                ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
                ("Lakshadweep","Lakshadweep"),("Puducherry","Puducherry"))

class Customer(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices = state_choices , max_length= 50)

    def __str__(self) :
        return str(self.id)
        

# product model

category_choices = (('M',"Mobile"),
                    ('L','Laptop'),
                    ('TW', 'Top Wear'),
                    ('BW', 'Bottom Wear'))

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices= category_choices)
    product_image = models.ImageField(upload_to = 'product image')

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    

# cart model 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) :
        return str(self.id)
    
    @property
    def total_cost(self):
        a = self.quantity * (self.product.selling_price-self.product.discounted_price)
        return a

# order placed model

status = (('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On the way','On the way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel')
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    razorpay_order_id=models.CharField(max_length=200,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=200,null=True,blank=True)
    razorpay_signature_id=models.CharField(max_length=200,null=True,blank=True)
    paid = models.BooleanField(default=False)
    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default=0)
    customer_name = models.CharField(max_length=200,null=True)
    locality = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=50,null=True)
    zipcode = models.IntegerField(null=True)
    state = models.CharField(choices = state_choices , max_length= 50,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices= status , default='pending')


