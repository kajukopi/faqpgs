from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db import models

class ImageUpload(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='imageuploads')
    img = models.FileField(upload_to='documents/')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'imageupload'
    
    def __str__(self):
        return f'{self.user}'

class Pertanyaan(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pertanyaans')
    pertanyaan_text = models.CharField(max_length=5000)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pertanyaan'

    def __str__(self):
        return self.pertanyaan_text

    def get_posts_count(self):
        return Komen.objects.filter(pertanyaan=self).count()

    def get_posts_list(self):
        context = {}
        context = Komen.objects.filter(pertanyaan=self)[0:2]
        return context

    # @admin.display(boolean=True,ordering='pub_date',description='Published recently?')

class Komen(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='komens')
    pertanyaan = models.ForeignKey(
        Pertanyaan, on_delete=models.CASCADE, related_name="komens")
    komen_text = models.CharField(max_length=5000)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'komen'

    def __str__(self):
        return f'{self.pertanyaan}'

    def get_data_pertanyaan(self):
        return Pertanyaan.objects.filter(pertanyaan_text=self)
