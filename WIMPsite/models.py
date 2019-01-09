from django.db import models

# Create your models here.


class TestStrip(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)


class ChemicalTest(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    test = models.ForeignKey(TestStrip, related_name='strip', on_delete=models.CASCADE)


class Color(models.Model):
    unit_value = models.IntegerField()
    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()

    text = models.CharField(max_length=30)

    test = models.ForeignKey(ChemicalTest, related_name='chemical_test', on_delete=models.CASCADE)


class ScheduledTest(models.Model):
    name = models.CharField(max_length=100)
    test_strip = models.ForeignKey(TestStrip, related_name='test', on_delete=models.CASCADE)
    last_run = models.DateTimeField()
    frequency = models.IntegerField()

