from django.db import models
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.urls import reverse
from django.core.files.storage import default_storage
import uuid
import os
import json
from django_quill.fields import QuillField





class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    profilepic = models.ImageField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.nickname

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
   
class Articlepost(models.Model):
    id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    short_description = QuillField()
    long_description = QuillField()
    slug = models.SlugField(max_length=255, null=True, blank=True,unique=True)
    postdate = models.DateField(null=True, blank=True)
    isfeature = models.BooleanField(blank=True,null=True)
    istrending = models.BooleanField(blank=True,null=True)
    tagify = models.CharField(max_length=200, blank=True, null=True)
    metatitle = models.CharField(max_length=160, blank=True, null=True)
    metatag = models.CharField(max_length=255, blank=True, null=True)
    metatagdescription  = models.TextField(max_length=250, blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(Author, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    view_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    def save(self,*args, **kwargs):
        if not self.slug or self.title != self.slug:
            self.slug = slugify(self.title)
        return super(Articlepost,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_tag_list(self):
        return json.loads(self.tagify)
    
    def get_absolute_url(self):
        # Replace 'your_view_name' with the actual name of your view
        return reverse('single', kwargs={'slug': self.slug})
    
    
class Affreg(models.Model):
    shopname = models.CharField(max_length=255, null=True, blank=True)
    shoplogo = models.CharField(max_length=255, null=True, blank=True)
    regid = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.affiliateshop

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    long_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='products/')
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g. 4.5
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    affiliate_url = models.URLField(help_text="Affiliate link to product (e.g. Amazon)")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metatitle = models.CharField(max_length=160, blank=True, null=True)
    metatag = models.CharField(max_length=255, blank=True, null=True)
    metatagdescription  = models.TextField(max_length=250, blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.short_description[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


def upload_to_location_for_affiliate(instance, filename):
    title = instance.folder
    folder_path = os.path.join('gallery/affiliate',title)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return os.path.join(folder_path,filename)

def upload_to_location_for_post(instance, filename):
    title = instance.folder
    folder_path = os.path.join('gallery/post',title)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    return os.path.join(folder_path,filename)


class Gallery(models.Model):
    title = models.CharField(max_length=100,null=True, blank=True)
    folder = models.CharField(max_length=100,null=True, blank=True) 
    image = models.ImageField(upload_to=upload_to_location_for_post, null=True,blank=True)
    alt = models.CharField(max_length=300 ,null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file from storage before deleting the instance
        if self.image:
            default_storage.delete(self.image.path)
        super().delete(*args, **kwargs)

