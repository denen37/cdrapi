from django.db import models

# Create your models here.
class Call(models.Model):
    callerName = models.CharField(max_length=100)
    callerNumber = models.CharField(max_length=20)
    receiverNumber = models.CharField(max_length=20)
    city=models.CharField(max_length=50)
    callDirection=models.BooleanField(default=False)
    callStatus=models.BooleanField(default=False)
    callDuration=models.IntegerField()
    # callCost=models.DecimalField(max_digits=10, decimal_places=2)
    callCost = models.FloatField()
    callStartTime=models.DateTimeField()
    callEndTime=models.DateTimeField()

    class Meta:
        db_table = "calls"
        managed = False

    def __str__(self):
        return f"{self.callerNumber} -> {self.receiverNumber}"
