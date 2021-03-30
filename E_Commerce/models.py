from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return  self.name


sub_category = (('Mens', 'Men'),
                ('Womens', 'Women'),
                ('Kids', 'Kids'),
                )
size = (('XXXXL', 'XXXXL'),
        ('XXXL', 'XXXL'),
        ('XXL', 'XXL'),
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
        ('XS', 'XS'),
        ('XS', 'XS'),
        ('XXS', 'XXS'),
        )


class Product(models.Model):
    title = models.CharField(max_length=128)
    company = models.CharField(max_length=128, default="Texile Ltd")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=200, choices=sub_category, default="", null=True,blank=True)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    alternative_text = models.CharField(max_length=200, default="", editable=False)
    size_5XL = models.IntegerField(default=0, null=True)
    size_4XL = models.IntegerField(default=0, null=True)
    size_3XL = models.IntegerField(default=0, null=True)
    size_XXL = models.IntegerField(default=0, null=True)
    size_XL = models.IntegerField(default=0, null=True)
    size_L = models.IntegerField(default=0, null=True)
    size_M = models.IntegerField(default=0, null=True)
    size_S = models.IntegerField(default=0,null=True)
    size_XS = models.IntegerField(default=0,null=True)
    size_XXS = models.IntegerField(default=0, null=True)
    p_quantity=models.IntegerField(default=0, null=True, verbose_name="quantity")
    total_quantity = models.IntegerField(default=0, editable=False)
    # size = models.CharField(max_length=10,choices=size,default="L")
    slug = models.SlugField(allow_unicode=True, null=True, blank=True, editable=False)
    upload_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_by_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    discount_by_value = models.IntegerField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def discount_calculation(self):
        if self.discount_by_percentage is None and self.discount_by_value is None and self.discount_price is None:
            return None
        elif self.discount_by_percentage is None and self.discount_by_value is None:
            return None
        else:
            discounted_value = 0
            if self.discount_by_percentage:
                discounted_value = (self.price * self.discount_by_percentage) / 100
                discounted_value = self.price - discounted_value
            else:
                if self.discount_by_value < self.price:
                    discounted_value = self.price - self.discount_by_value

        return discounted_value

    def quantity(self):
        total = self.size_5XL + self.size_4XL + self.size_3XL + self.size_XXL + self.size_XL + self.size_L + self.size_M + self.size_S + self.size_XS + self.size_XXS
        return total

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = f'images/Products/{self.category}/{self.title}/'

        if not self.slug:
            self.slug = slugify(self.title)

        value = self.discount_calculation()
        if value is not None:
            self.discount_price = value
        else:
            self.discount_price = None

        total = self.quantity()
        total+=self.p_quantity
        self.total_quantity = total
        self.alternative_text = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HomeBanner(models.Model):
    name = models.CharField(max_length=128)
    body = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/HomeBanner/')
    slug = models.SlugField(allow_unicode=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    alternative_text = models.CharField(default='', max_length=200, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + str(self.id))
        self.alternative_text = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/UserProfile/', default="images/default_profile_pic/default-profile.jpg")
    alternative_text = models.CharField(max_length=200, editable=False)

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = f'images/UserProfile/{self.user.username}/'

        self.alternative_text = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    # def save(self,*args,**kwargs):
    #     for field in self._meta.fields:
    #         if field.name == "product":
    #             pass

# class Order(models.Model):
#     cart_item = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     total_quantity = models.PositiveIntegerField()
#     order_placed_date = models.DateTimeField(auto_now_add=True)
#
#     def save(self, *args, **kwargs):
#         for field in self._meta.fields:
#             if field.name == "total_quantity":
#                 prod_quantity = Cart.quantity
#                 if self.total_quantity > 0:
#                     self.total_quantity += prod_quantity
#                 else:
#                     self.total_quantity = prod_quantity
#         super(Order, self).save(*args, **kwargs)
