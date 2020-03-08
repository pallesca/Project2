from django.contrib.auth.models import AbstractUser
from django.db import models


# Vlad feedback: create a many to many relationship for the watchlist under user
class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watchlist", blank=True)

#auctions
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length = 500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner", null=True)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)

    def __str__(self):return f"{self.title} "

    def get_cat_list(self):
        k = self.category 
        
        #categories
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

#category
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True ,related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

#comment
class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name="comment_listing")
    comment = models.TextField(max_length=400)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_owner",default=1)

    def __str__(self):
        return f"{self.headline} ({self.owner.username})"
# bid
# class Bid(models.Model):
#   owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner", null=True)
#   listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
#   bid_time = models.DateTimeField()
