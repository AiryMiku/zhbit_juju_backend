from django.db import models
from apps.Utils.DateTimeUtil import format_datetime_to_str

# Create your models here.

# 交流


class User(models.Model):
    # 基本信息
    account_name = models.CharField(max_length=40)  # 账户名(登陆用)
    password = models.CharField(max_length=40)  # 密码 使用md5 16进制存储
    nickname = models.CharField(max_length=40)  # 昵称

    access_token = models.CharField(max_length=100,default = "0")  #

    # 拓展信息
    sex = models.IntegerField(default=-1)  # -1 = 未编辑 0 = 女 1 = 男
    birth = models.DateField(default='')  # 生日
    phone = models.IntegerField(default=10010)  # 电话号码
    status = models.CharField(max_length=100,default='')  # 签名

    # 隐私
    enable_searched = models.BooleanField(default=True)  # 是否允许被搜索
    enable_visited_list = models.IntegerField(default=15)  # 允许被查看的拓展信息列表 二进制维护

    def to_list_dict(self):
        dict_data={
            'id':self.id,
            'nickname':self.nickname,
            'sex':self.sex,
            'birth':self.birth,
            'phone': self.phone,
            'status': self.status,
        }
        return dict_data


# 信息
class Message(models.Model):
    message_type = models.IntegerField(default=0)  # 0 = 群体信息  1 = 个人信息
    from_id = models.IntegerField(default=0)  # 根据type的类型 id 为 群组id or 用户id
    to_id = models.IntegerField(default=0)  # 如果type = 0 则 to_id = 0 否则为对应用户的id
    context = models.CharField(max_length=140)  # 信息文本


# 关注关系 不论谁关注谁，每两个人只有一行数据
class FollowMapping(models.Model):
    user_left_id = models.IntegerField(default=0)  # 左用户的id
    user_right_id = models.IntegerField(default=0)  # 右用户的id
    left_to_right = models.BooleanField(default=False)  # 左是否关注右
    right_to_left = models.BooleanField(default=False)  # the same


# 通知推送消息
class Notification(models.Model):
    Notification_type = models.IntegerField(default=0)  # 推送消息的类型 0 = 群组成员变动 1 = 活动更改 2 = 被关注
    Notification_text = models.CharField(max_length=200)  # 通知信息的文本


# 权限
class Permissions(models.Model):
    # 权限列表
    role = models.IntegerField(default=0)  # 权限组角色 1 = 群主 2 = 管理员 3 = 普通用户
    # 群组
    modify_group = models.BooleanField(default=False)  # 修改群组信息的权限
    set_admin = models.BooleanField(default=False)  # 设置管理员
    send_group_message = models.BooleanField(default=False)  # 发送信息给群体成员

    def to_list_dict(self):
        dict_data={
            'modify_group':self.modify_group,
            'set_admin':self.set_admin,
            'send_group_message':self.send_group_message,
        }
        return dict_data

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
            'create_time': format_datetime_to_str(self.create_time)
        }
        return dict_data


# 关注群组映射
class UserFollowGroupMapping(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)  # user_id
    role = models.IntegerField(default=0)  # user_role_in_group


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
            'start_time': format_datetime_to_str(self.start_time),
            'end_time': format_datetime_to_str(self.end_time),
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
            'time': format_datetime_to_str(self.time)
        }
        return dict_data


# 评论活动映射表
class ActivityBelongComment(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)

# 信息分享 End
