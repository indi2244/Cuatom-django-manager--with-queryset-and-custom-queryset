from django.db import models
from django.db.models import Count
#not over ridden query set

class SchoolQuerySet(models.QuerySet):
    def by_name(self, school_name):
        return self.filter(name= school_name)

    def established_after(self, year):
        return self.filter(established_date__year__gt=year)
        
class SchoolManager(models.Manager):
    def get_queryset(self):
        return SchoolQuerySet(self.model, using=self._db)

    def by_name(self,school_name):
        return self.get_queryset().by_name(school_name)
    
    def established_after(self, year):#chainable queryset
        return self.get_queryset().established_after(year)
    
    #overridden queryset
class School_1988_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(established_date__year=1988)
    
#overridden queryset and adding multiple managers
class School_1988_before_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(established_date__year__lt=1988) #lt is less than
    
#overridden queryset
class School_1988_after_Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(established_date__year__gt=1988) #lt is greater than

class School(models.Model):
    name = models.CharField(max_length=20)
    principal = models.CharField(max_length=20)
    established_date = models.DateField()
    objects = models.Manager()
    school_objects= SchoolManager()

    school_1988 = School_1988_Manager()
    school_before_1988= School_1988_before_Manager()
    school_after_1988= School_1988_after_Manager()


    def __str__(self):
        return self.name


class BookManager(models.Manager):# advanced query with annotation
    def count_books_by_author(self):
        return self.values('author').annotate(book_count=Count('id'))
    
    def total_books(self):#advanced query with aggregation
        return self.aggregate(total_count=Count('id'))

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    # Add the custom manager
    objects = BookManager()

    def __str__(self):
        return self.title

class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role="A")

    def editors(self):
        return self.filter(role="E")

class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def authors(self):
        return self.get_queryset().authors()

    def editors(self):
        return self.get_queryset().editors()

class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")


class EditorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="E")


'''Public methods are copied by default.

Private methods (starting with an underscore) are not copied by default.

Methods with a queryset_only attribute set to False are always copied.

Methods with a queryset_only attribute set to True are never copied.'''
class CustomQuerySet(models.QuerySet):
    # Available on both Manager and QuerySet.
    def public_method(self):
        return self.filter(role="A")

    # Available only on QuerySet.
    def _private_method(self):
        return self.filter(role="E")

    # Available only on QuerySet.
    def opted_out_public_method(self):
        return self.filter(name__startswith="J")

    opted_out_public_method.queryset_only = True

    # Available on both Manager and QuerySet.
    def _opted_in_private_method(self):
        return self.filter(role="A")

    _opted_in_private_method.queryset_only = False

class Person(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices={"A": ("Author"), "E": ("Editor")})
    people = models.Manager()
    humans=PersonManager()
    worker = CustomQuerySet.as_manager()
    authors = AuthorManager()
    editors = EditorManager()

    def __str__(self):
        return self.name