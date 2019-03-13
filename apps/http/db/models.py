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
class Chitchat(models.Model):
    # 会话主要信息
    chitchat_name = models.CharField(max_length=30)  # 会话名称
    chitchat_type = models.IntegerField(default=-1)  # 会话类别 0 = 个人会话 1 = 群聊
    chitchat_owner = models.CharField(max_length=40)  # 会话归属 个人会话 记录两个人的id 群聊 记录所属群组的id
    # 群聊信息
    chitchat_manager = models.CharField(max_length=200)  # 群管理员的id列表


# 聊天记录
class ChatRecord(models.Model):
    # 记录信息
    chatrecord_owner = models.IntegerField(default=0)  # 所属会话 id
    chatrecord_type = models.IntegerField(default=0)  # 记录类型 0 = 个人会话 1 = 群聊
    chatrecord_text = models.CharField(max_length=300)  # 文本


# 通知推送消息
class Notification(models.Model):
    Notification_type = models.IntegerField(default=0)  # 推送消息的类型


# 权限
# class Permissions(models.Model):

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
            'id': self.id,
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
            'id': self.id,
            'title': self.title,
            'content': self.content,
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

    def to_list_dict(self):
        dict_data = {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'time': self.time
        }
        return dict_data


# 评论活动映射表
class ActivityBelongComment(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)

# 信息分享 End
