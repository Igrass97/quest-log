# Models and Queries

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
