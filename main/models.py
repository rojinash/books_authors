from django.db import models
import re
import bcrypt


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    notes = models.TextField()
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 1:
            errors['first_name'] = "Please provide a first name"
        if len(post_data['last_name']) < 1:
            errors['last_name'] = "Please provide a last name"
        # if len(post_data['email']) < 1:
        #     errors['email'] = "Please provide an email"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email'
        if len(post_data['password']) < 4:
            errors['password'] = "Please provide a longer password"
        if post_data['password'] != post_data['confirm_pw']:
            errors['confirmation'] = "Password confirmation does not match password"
        return errors
    def login_validator(self, post_data):
        result = {'err_log' : [], 'status' : False}
        registered_user = User.objects.filter(email=post_data['email'])

        if registered_user.count() == 0:
            result['err_log'].append('This user is not registered')
        else:
            if bcrypt.checkpw(post_data['password'].encode(), registered_user[0].password.encode()):
                result['status'] = True
                result['user_id'] = registered_user[0].id
            else:
                result['err_log'].append('Incorrect password')
        return result
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=78)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
