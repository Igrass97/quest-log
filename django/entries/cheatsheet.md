# Models

## Defining models

Models inherits from `models.Model`.

Model's fields are fields in the database

Fields are defined using a `Field` class like `CharField` (imported from models) https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types

Models can have methods

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

        def get_full_name(self):
            return self.first_name + self.last_name

## Create instance and save to DB

Simply instanciate the class and call `.save()`

    from models import Person

    p = Person(first_name='Ignacio', last_name='Grassini')
    p.save()

## Relationships

### One to Many

`django.db.models.ForeignKey`

A one-to-many relationship is a relationship where each record in the first table can correspond to many records in the second table, but each record in the second table corresponds to only one record in the first table.

For example, if a Car model has a Manufacturer – that is, a Manufacturer makes multiple cars but each Car only has one Manufacturer – use the following definitions:

    from django.db import models

    class Manufacturer(models.Model):
        name = models.CharField(max_length=30)

    class Car(models.Model):
        manufacturer = models.ForeignKey(Manufacturer)
        name = models.CharField(max_length=30)

#### Reverse relationships

    from models import Manufacturer, Car

    m = Manufacturer(name="Toyota")
    m.save()

    c1 = Car(name="Corolla", manufacturer_id=m.id)
    c2 = Car(name="Yaris", manufacturer_id=m.id)
    c1.save()
    c2.save()

    m.car_set.all()
    m.car_set.filter()
    m.car_set.count()

Also, the Manufacturer class can call the following methods to add cars to the car_set:

Adds the specified model objects to the related object set

    add(obj1, obj2, ...)

Creates a new object, saves it and puts it in the related object set. Returns the newly created object.

    create(**kwargs)

Removes the specified model objects from the related object set.

    remove(obj1, obj2, ...)

Removes all objects from the related object set.

    clear()

Replace the set of related objects.

    set(objs)

### Many To Many

`django.db.models.ManyToManyField`

A many-to-many relationship is a relationship where each record in the first table can correspond to many records in the second table, and vice versa.

Each student can enroll in multiple courses, and each course can have multiple students enrolled.

    class Student(models.Model):
        name = models.CharField(max_length=100)
        courses = models.ManyToManyField(Course, related_name='students')

    class Course(models.Model):
        name = models.CharField(max_length=100)

#### Reverse relationships

Course -> Students

    # get a course object
    course = Course.objects.get(pk=1)

    # access all students enrolled in the course
    students = course.students.all()

Student -> Courses

    # get a student object
    student = Student.objects.get(pk=1)

    # access all courses that the student is enrolled in
    courses = student.courses.all()

#### Using an intermediary model

It's useful when you want to define extra fields in the relationship

    from django.db import models

    class Person(models.Model):
        name = models.CharField(max_length=128)

        def __str__(self):
            return self.name

    class Group(models.Model):
        name = models.CharField(max_length=128)
        members = models.ManyToManyField(Person, through='Membership')

        def __str__(self):
            eturn self.name

    class Membership(models.Model):
        person = models.ForeignKey(Person, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)
        date_joined = models.DateField()
        invite_reason = models.CharField(max_length=64)

### One-To-One

`django.db.models.OneToOne`

This is most useful on the primary key of an object when that object “extends” another object in some way.

    class Person(models.Model):
        name = models.CharField(max_length=100)

    class Profile(models.Model):
        person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='profile')
        bio = models.TextField()

#### Reverse relationships

Person -> Profile

    # get a person object
    person = Person.objects.get(pk=1)

    # access the associated profile object
    profile = person.profile

    # print the bio of the person's profile
    print(profile.bio)

Profile -> Person

    # get a profile object
    profile = Profile.objects.get(pk=1)

    # access the associated person object
    person = profile.person

    # print the name of the person
    print(person.name)

## Meta options

Is anything that is not a field.

[All meta options](https://docs.djangoproject.com/en/4.1/ref/models/options/)

    from django.db import models

    class Ox(models.Model):
        horn_length = models.IntegerField()

        class Meta:
            ordering = ["horn_length"]
            verbose_name_plural = "oxen"
            db_table = "oxen"

## Manager

Is the interface through which database query operations are provided to Django models. Mainly used to retrieve the instances from the database. The default manager is `Model.objects`

    from myapp.models import MyModel

    # Retrieve all objects of MyModel
    all_objects = MyModel.objects.all()

    # Retrieve a specific object of MyModel based on its primary key (id)
    object_with_id_1 = MyModel.objects.get(id=1)

    # Retrieve objects of MyModel based on some other criteria
    objects_with_field_value = MyModel.objects.filter(field_name=value)


    # Create a new object of MyModel
    new_object = MyModel(field_name_1=value_1, field_name_2=value_2)

    # Save the new object to the database
    new_object.save()

    # Create and save a new object of MyModel using the create() method
    new_object = MyModel.objects.create(field_name_1=value_1, field_name_2=value_2)

## Model Instance Methods

Model methods act in a particular instance.

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
        age = models.IntegerField(min=0)

        def can_drink(self):
            return self.age >= 18

        @property
        def full_name(self):
            return '%s %s' % (self.first_name, self.last_name)

[All model instance methods](https://docs.djangoproject.com/en/4.1/ref/models/instances/#model-instance-methods)

### Probably always need to define these methods

`__str__()` returns a string representation of any object.
`get_absolute_url()` tells Django how to calculate the URL for an object.

### Override Instance Methods

Often, you'll want to change the way an object is saved or deleted, you can override this behaviour.

    from django.db import models

    class Person(models.Model):
        ...fields

        def save(self, *args, **kwargs):
            something()
            super().save(*args, **kwargs) # Call the models.Model.save() method

## Model Class Methods

    from django.db import models
    from datetime import date

    class Person(models.Model):
        name = models.CharField(max_length=100)
        birthdate = models.DateField()

    @classmethod
    def get_average_age(cls):
        today = date.today()
        total_age = 0
        num_people = cls.objects.count()
        for person in cls.objects.all():
            total_age += # calculate age in current person
        return total_age / num_people if num_people else 0

Instead of adding the method as a static method of the class, creating a new Manager is preferred.

    from django.db import models

    class PersonManager(models.Manager):
            def get_average_age(self):
                today = date.today()
                total_age = 0
                num_people = self.count()
                for person in self.all():
                    total_age += # calculate age in current person
                return total_age / num_people if num_people else 0

## Model Inheritance

### 1. Hold common information (Abstract Class)

This model will then not be used to create any database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child class.

    from django.db import models

    class CommonInfo(models.Model):
        name = models.CharField(max_length=100)
        age = models.PositiveIntegerField()

        class Meta:
            abstract = True
            this_field_will_be_inherited_as_well = True

    class Student(CommonInfo):
        home_group = models.CharField(max_length=5)

    class Teacher(CommonInfo):
        area = models.CharField(max_length=30)

If you inherit from multiple abstract models, Python will only inherit the `Meta` of the first class passed. So if you want to inherit `Meta` from multiple classes, you'll have to set it explicitly.

    from django.db import models

    class Person(models.Model):
        Meta(Model1.Meta, Model2.Meta):
            ...

### 2. Multi-table inheritance

Each model corresponds to its own database table and can be queried and created individually.

The inheritance relationship introduces links between the child model and each of its parents (via an automatically-created OneToOneField).

    from django.db import models

    class Place(models.Model):
        name = models.CharField(max_length=50)
        address = models.CharField(max_length=80)

    class Restaurant(Place):
        serves_hot_dogs = models.BooleanField(default=False)
        serves_pizza = models.BooleanField(default=False)

    Place.objects.filter(name="Bob's Cafe")
    Restaurant.objects.filter(name="Bob's Cafe")

### 3. Proxy models

They can change the behaviour of the parent model without creating a new table.

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

    class MyPerson(Person):
        class Meta:
            ordering = ["last_name"]
            proxy = True

    def do_something(self):
        # ...
        pass

# Queries

## Creating

`model_instance.save()` or `MyModel.objects.create(...values)`

## Updating

`model_instance.field1 = 'new_value'` and `model_instance.save()`

### Update ForeignKey

`model_instance1.foreign_field = model_instance2`

### Update ManyToManyField

`model_instance1.many_to_many_field.add(model_instance2)`

## Query Sets (retrieving)

### All

`all_records = MyModel.objects.all()`

### Filters

`filtered_records = MyModel.filter(lookup_field=lookup_value)`

`non_excluded_records = MyModel.exclude(exclude_field=exclude_value)`

### Single object

`single_record = MyModel.objects.get(pk=1)`

[All QuerySet methods](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#queryset-api)

### Limiting QuerySets

`limited_records = MyModel.objects.all()[:5]`

Translates into `LIMIT 5` so it's still performant! (you're not really retrieving `all()` objects)

### Field lookups

They're specified as keyword arguments to the QuerySet methods `filter(), exclude() and get()`

`field__lookuptype=value`

`people_that_can_drink` = Person.objects.filter(age\_\_gte=18)`

[All Field Lookup Types](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups)

### JOINs

    from django.db import models
    class Blog(models.Model):
        name = models.CharField(max_length=30)

    class Entry(models.Model):
        blog = models.ForeignKey(Blog)

`Entry.objects.filter(blog__name='Beatles Blog')`

`Blog.objects.filter(entry__headline__contains='Lennon')`
