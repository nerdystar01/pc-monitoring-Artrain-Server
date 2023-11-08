from django.db import models

# Create your models here.

class Pc(models.Model):
    username = models.CharField(default='', max_length=100)
    password = models.CharField(default='', max_length=10)
    start_at = models.DateTimeField(auto_now=True)
    url = models.URLField(default='', blank=True)
    seat = models.CharField(default='', blank=True, max_length= 200)
    status = models.BooleanField(default= True) # True: 사용가능 / False: 사용불가능

    class Meta:
        db_table = "pc"
        verbose_name = "피씨"
        verbose_name_plural = verbose_name
        

# class UseHistory(models.Model):
#     pc = models.ForeignKey(Pc, on_delete=models.CASCADE)
#     username = models.CharField(default='', max_length=100)
#     password = models.CharField(max_length=4)
#     start_at = models.DateTimeField(auto_now_add= True)
#     end_at = models.DateTimeField(auto_now=True)
#     status = models.BooleanField(default= True) # True: 사용즁 / False: 사용완료.

#     class Meta:
#         db_table = "use_history"
#         verbose_name = "사용 이력"
#         verbose_name_plural = verbose_name
        

