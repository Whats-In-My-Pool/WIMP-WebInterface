from django.db import models

# Create your models here.


class TestStrip(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)


class ChemicalTest(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    test = models.ForeignKey(TestStrip, related_name='tests', on_delete=models.CASCADE)


class Color(models.Model):
    unit_value = models.FloatField()
    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()

    text = models.CharField(max_length=30)

    test = models.ForeignKey(ChemicalTest, related_name='colors', on_delete=models.CASCADE)

    @property
    def html_color(self):
        r = format(self.r, "x")
        g = format(self.g, "x")
        b = format(self.b, "x")

        return "#{}{}{}".format(r, g, b)


class ScheduledTest(models.Model):
    time_scale = (
        ('H', 'Hour'),
        ('D', 'Day'),
        ('W', 'Week')
    )

    name = models.CharField(max_length=100)
    test_strip = models.ForeignKey(TestStrip, related_name='strip', on_delete=models.CASCADE)
    last_run = models.DateTimeField()
    frequency = models.IntegerField()
    scale = models.CharField(max_length=1, choices=time_scale)
