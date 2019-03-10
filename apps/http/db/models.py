from django.db import models


# Create your models here.

# 交流

class User(models.Model):
    # 基本信息
    account_name = models.CharField(max_length=40)  # 账户名(登陆用)
    password = models.CharField(max_length=40)  # 密码 使用md5 16进制存储
    nickname = models.CharField(max_length=40)  # 昵称
    info_visibility = models.IntegerField(default=0)


# 聊天会话
# class Session(models.Model):
# 通知推送消息
# class Notification(models.Model):
# class permissions(models.Model):

# 交流 End

# 信息分享
# 群组
class Group(models.Model):
    owner_user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=40)  # 群组名称
    notice = models.CharField(max_length=240, default='未有公告')  # 公告
    introduction = models.CharField(max_length=240)  # 简介
    create_time = models.DateTimeField(default=None)

    # to dict for display

    def to_list_dict(self):
        dict_data = {
            'group_id': self.id,
            'owner_user_id': self.owner_user_id,
            'name': self.name,
            'notice': self.notice,
            'introduction': self.introduction,
            'create_time': str(self.create_time)
        }
        return dict_data


# 关注群组映射
class UserFollowGroupMapping(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)  # group_id
    user = models.ForeignKey("User", on_delete=models.CASCADE)  # user_id


# 活动
class Activity(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    place = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    like_number = models.IntegerField(default=0)

    def to_list_dict(self):
        dict_data = {
            'activity_id': self.id,
            'title': self.title,
            'place': self.place,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'like_number': self.like_number
        }
        return dict_data


# 参加活动映射
class UserAttendActivityMapping(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)


# 活动从属群组映射表
class ActivityBelongGroupMapping(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)  # group_id
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)


# like映射表, 存在便有like，不存在便无
class ActivityLikeMapping(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)


# 评论
class Comment(models.Model):
    user_id = models.IntegerField(default=0)  # user_id
    content = models.CharField(max_length=120)
    time = models.DateTimeField()


# 评论活动映射表
class ActivityBelongComment(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)

# 信息分享 End
