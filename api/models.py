from django.db import models

class SentencePair(models.Model):
    sentence1 = models.CharField(max_length=256)
    sentence2 = models.CharField(max_length=256)
    score = models.FloatField()
