from math import sqrt

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


class TestResult(models.Model):
    chemical_test = models.ForeignKey(ChemicalTest, related_name="results", on_delete=models.PROTECT)
    color_match = models.ForeignKey(Color, related_name="results", on_delete=models.PROTECT)
    time_run = models.DateTimeField()

    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()

    @staticmethod
    def get_color_match(chemical_test_id, r, g, b):
        test = ChemicalTest.objects.get(pk=chemical_test_id)

        min_distance = 1000
        color_match = None

        for color in test.colors.all():
            distance = sqrt((color.r - r) ** 2 + (color.g - g) ** 2 + (color.b - b) ** 2)

            if distance < min_distance:
                min_distance = distance
                color_match = color

        return color_match
