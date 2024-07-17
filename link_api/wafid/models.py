from django.db import models
from authentication.models import User



class CardInfoModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    name_on_card = models.CharField(max_length=250)
    card_no = models.CharField(max_length=30)
    exp_date = models.CharField(max_length=8)
    cvv_cvc = models.CharField(max_length=8)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    otp_mobile_link = models.URLField()
    otp_email_link = models.URLField()

    def __str__(self):
        return f"{self.title} - {self.name_on_card}"


