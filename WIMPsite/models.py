from django.db import models
from django.conf import settings
from WIMPsite.color_match import get_delta_e


# Create your models here.


class TestStrip(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def is_current_test(self):
        count = ScheduledTest.objects.filter(test_strip_id=self.id, current_test=True).count()

        if count:
            return True
        else:
            return False


class ChemicalTest(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=30)
    test = models.ForeignKey(TestStrip, related_name='tests', on_delete=models.CASCADE)
    invert_color_match = models.BooleanField(default=False)
    test_number = models.IntegerField()

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


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

    @property
    def rgb(self):
        return self.r, self.b, self.g

    @property
    def shifted_color(self):
        shift = getattr(settings, "COLOR_SHIFT", (0, 0, 0))

        return self.r - shift[0], self.g - shift[1], self.b - shift[2]

    def __str__(self):
        return "Color {} ({} {} {}) ({})".format(self.text, self.r, self.g, self.b, self.id)


class ScheduledTest(models.Model):
    time_scale = (
        ('H', 'Hour'),
        ('D', 'Day'),
        ('W', 'Week')
    )

    name = models.CharField(max_length=100)
    test_strip = models.ForeignKey(TestStrip, related_name='strip', on_delete=models.CASCADE)
    last_run = models.DateTimeField(null=True)
    frequency = models.IntegerField()
    scale = models.CharField(max_length=1, choices=time_scale)
    current_test = models.BooleanField()

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class TestResult(models.Model):
    chemical_test = models.ForeignKey(ChemicalTest, related_name="results", on_delete=models.PROTECT)
    time_run = models.DateTimeField()

    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()

    @property
    def rgb(self):
        return self.r, self.b, self.g

    @property
    def get_top_matches(self):
        color_matches = self.get_color_match
        error = abs((color_matches[0][1] - color_matches[1][1]) / color_matches[0][1])

        if error < 0.25:
            return color_matches[0][0], color_matches[1][0]
        else:
            return color_matches[0][0], None

    @property
    def html_color(self):
        r = format(self.r, "x")
        g = format(self.g, "x")
        b = format(self.b, "x")

        return "#{}{}{}".format(r, g, b)

    @property
    def get_color_match(self):
        color_list = []

        for color in self.chemical_test.colors.all():
            rgb = color.shifted_color
            distance = get_delta_e(rgb, (self.r, self.g, self.b))

            color_list.append((color, distance))

        color_list.sort(key=lambda tup: tup[1])

        return color_list


class TempResult(models.Model):
    time = models.DateTimeField(auto_now=True)
    temp = models.FloatField()

    @property
    def temp_to_f(self):
        return (self.temp * 1.8) + 32
