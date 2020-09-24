from django.db import models


# Create your models here.
class Users(models.Model):
    GENDER = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知'),
    )
    nickname = models.CharField(max_length=32, db_index=True)
    phonenum = models.CharField(max_length=16, db_index=True, unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=16, choices=GENDER,default='unknown')
    location = models.CharField(max_length=32)
    avatar = models.CharField(max_length=128)

    class Meta:
        db_table='users'

    def userInfo(self):
        data={
            'id': self.id,
            'nickname' : self.nickname,
            'phonenum' : self.phonenum,
            'birthday' : self.birthday,
            'gender' : self.gender,
            'location' : self.location,
            'avatar' : self.avatar,
        }
        return data