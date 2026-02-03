from django.db import models

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name="subcounties"
    )
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('county', 'name')

    def __str__(self):
        return f"{self.name} ({self.county.name})"


class Ward(models.Model):
    subcounty = models.ForeignKey(
        SubCounty,
        on_delete=models.CASCADE,
        related_name="wards"
    )
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('subcounty', 'name')

    def __str__(self):
        return f"{self.name} ({self.subcounty.name})"
