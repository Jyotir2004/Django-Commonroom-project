from django.db import models
from django.db.models.functions import Lower
from django.conf import settings

# Create your models here.



class student(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField()
    role = models.CharField(max_length=50, blank=True, null=True)
    team = models.CharField(max_length=50, blank=True, null=True)
    invited_at = models.DateTimeField(auto_now_add=True)
    address=models.TextField(null=True, blank=True)
    file=models.FileField(upload_to='files/', blank=True, null=True)
    pin=models.CharField(max_length=10, blank=True, null=True)



class car(models.Model):
    MAKES = [
        ('Maruti Suzuki', 'Maruti Suzuki'),
        ('Hyundai', 'Hyundai'),
        ('Toyota', 'Toyota'),
    ]

    car_name = models.CharField(max_length=500, choices=MAKES)
    speed = models.IntegerField(default=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.car_name


class product(models.Model):
    pass


class MemberStatus(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='member_status',
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} - {"Active" if self.is_available else "Inactive"}'


class WorkspaceInvite(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workspace_invites',
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=100, default='Team member')
    team = models.CharField(max_length=100, default='Unassigned')
    invited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                'owner',
                name='unique_workspace_invite_email_per_owner',
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.email})'