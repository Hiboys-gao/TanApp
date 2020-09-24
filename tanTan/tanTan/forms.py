from django import forms

from UserApp.models import Users, Profile


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['nickname', 'birthday', 'gender', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


    def clean_min_distance(self):
        clean_data=super().clean()
        max_distance=clean_data['max_distance']
        min_distance=clean_data['min_distance']
        if max_distance < min_distance:
            raise forms.ValidationError('最小距离不能大于最大距离')
        else:
            return min_distance

    def clean_min_dating_age(self):
        clean_data=super().clean()
        max_dating_age=clean_data['max_dating_age']
        min_dating_age=clean_data['min_dating_age']
        if min_dating_age > max_dating_age:
            raise forms.ValidationError('最小年龄不能大于最大年龄')
        else:
            return min_dating_age