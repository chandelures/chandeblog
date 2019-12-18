from django import forms

from userprofile.models import User


class ProfileForm(forms.Form):
    class Meta:
        # 关联的数据库模型，这里是用户模型
        model = User
        # 前端显示、可以修改的字段（admin中）
        fields = ['nickname''link', 'avatar']
