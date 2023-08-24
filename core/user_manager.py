from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_superuser(self,email,password,**extra_fields):
        user = self.create(email=email,password=password,**extra_fields)
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user
