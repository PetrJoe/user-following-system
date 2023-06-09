from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f'{self.user.email}  -------- follows --------  {self.follower.email}'
    