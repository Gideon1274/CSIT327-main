from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		
		return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, default="Default")

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    if created:
        
        Customer.objects.create(user=instance, name=instance.username, email=instance.email)
    else:
        
        customer, _ = Customer.objects.get_or_create(user=instance)
        customer.name = instance.username
        customer.email = instance.email
        customer.save()

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='products/')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products')
	description = models.CharField(max_length=200, null=True, default="") 

	def __str__(self):
		return self.name
	def average_rating(self):
		reviews = ProductReview.objects.filter(product=self)
		if reviews.exists():
			avg = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
			return avg
		return 0
	
	def display_average_stars(self):
		avg = int(self.average_rating())
		filled_stars = '★' * avg
		empty_stars = '☆' * (5 - avg)
		return filled_stars + empty_stars

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, default=None)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		if self.product is not None:
			total = self.product.price * self.quantity
			return total
		else:
			return 0
	def __str__(self):
		return self.product.name
	
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
	

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review = models.CharField(max_length=200, null=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def display_stars(self):
        filled_stars = '★' * self.rating  # Filled stars
        empty_stars = '☆' * (5 - self.rating)  # Empty stars
        return filled_stars + empty_stars

    def __str__(self):
        return self.review
