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
    birthday = models.DateField(max_length=16, default='2000-01-01')
    gender = models.CharField(max_length=16, choices=GENDER, default='unknown')
    location = models.CharField(max_length=16, default='上海')
    avatar = models.CharField(max_length=128, default='#')

    class Meta:
        db_table = 'users'

    @property
    def profile(self):
        if not hasattr(self, 'ownProfile'):
            self.ownProfile, create = Profile.objects.get_or_create(id=self.id)
        return self.ownProfile

    def to_dict(self):
        data = {
            'id': self.id,
            'nickname': self.nickname,
            'phonenum': self.phonenum,
            'birthday': self.birthday,
            'gender': self.gender,
            'location': self.location,
            'avatar': self.avatar,
        }
        return data


class Profile(models.Model):
    """
        dating_gender      Yes      str       匹配的性别
        dating_location    Yes      str       ⽬标城市
        max_distance       Yes      float     最⼤查找范围
        min_distance       Yes      float     最⼩查找范围
        max_dating_age     Yes      int       最⼤交友年龄
        min_dating_age     Yes      int       最⼩交友年龄
        vibration          Yes      bool      开启震动
        only_matched       Yes      bool      不让为匹配的⼈看我的相册
        auto_play          Yes      bool      ⾃动播放视频
        """
    dating_gender = models.CharField(max_length=16, default='女')
    dating_location = models.CharField(max_length=16, default='上海')
    max_distance = models.IntegerField(default=5)
    min_distance = models.IntegerField(default=1)
    max_dating_age = models.IntegerField(default=30)
    min_dating_age = models.IntegerField(default=18)
    vibration = models.BooleanField(default=True)
    only_matched = models.BooleanField(default=True)
    auto_play = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile'

    def to_dict(self):
        data = {
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'max_distance': self.max_distance,
            'min_distance': self.min_distance,
            'max_dating_age': self.max_dating_age,
            'min_dating_age': self.min_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
        return data