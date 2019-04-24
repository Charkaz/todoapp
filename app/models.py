from django.db import models

class newtasks(models.Model):
    author = models.ForeignKey("auth.User",on_delete= models.CASCADE)
    title = models.CharField(max_length= 50)
    text = models.TextField()
    deadline = models.DateField(null=False , verbose_name="Son tarix")
    created_date = models.DateField(auto_now_add=True)

    paylasan = models.CharField(max_length= 50)
    
    def __str__(self):
        return self.title



class serhs(models.Model):
    task = models.ForeignKey(newtasks,on_delete= models.CASCADE)
    serh = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=50)



