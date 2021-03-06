# zhbit_juju_backend - python3

Django / miniconda - https://docs.conda.io/en/latest/miniconda.html
```shell
    conda create -n juju
    conda activate juju
    conda install -c anaconda django
    pip install mysqlpython
    pip install sqlparse
    pip install channels
```


Mysql 
```sql
    CREATE DATABASE 'juju';
    CREATE USER 'juju'@'localhost' IDENTIFIED BY '1234';
    GRANT ALL PRIVILEGES ON `juju`.* to 'juju'@'localhost';
 ```
 
 
 DB schema migration - 
 ```shell
   python manage.py makemigrations
   
       - Create model Activity
    - Create model Comment
    - Create model FollowMapping
    - Create model Group
    - Create model Message
    - Create model Notification
    - Create model Permissions
    - Create model User
    - Create model UserFollowGroupMapping
    - Create model UserAttendActivityMapping
    - Create model ActivityLikeMapping
    - Create model ActivityBelongGroupMapping
    - Create model ActivityBelongComment
    
    
   python manage.py migrate
   python manage.py runserver
 ```
 
 

    
# 约定
### 分支
* master
* dev_airy
* tph

### request_key_dict 规定
```json
{
  "[request_param_key]": "validate_rule" 
}
```

### 标准返回格式
```json
{
  "code": 0,
  "data": {
    ...
  }
}
```
```json
{ // 有列表数据的时候
  "code": 0,
  "data": {
    "count": 1,
    "list": [
      ...
    ]
  }
}
```

### 一些规范
* 所有返回的实体信息统称id,详细见apps/db/model.py,减少信息冗余，便于客户端对接（写少点实体

## 已知bug懒得修
* 查询没有的东西会直接boom（迟点再修

## 群组（前缀 group/
* 创建群组 （已测试）
    * path('create/', GroupController.create), 
* 删除群组（未加入权限控制，测试可以删除
    * path('delete/', GroupController.delete), 
* 修改群组（已测试
    * path('modify/', GroupController.modify),
### Member Manger
* 设置管理员（等权限模块
    * path('setAdmin/', GroupController.set_admin),
* 邀请人员（等通知模块
    * path('invite/', GroupController.invite),
* 移除人员（
    * path('remove_member/', GroupController.remove_member),
### Query
* 查看所有群组（已测试
  * path('indexAll/', QueryController.index),

返回Json
```json
{
    "code": 0,
    "data": {
        "count": 8,
        "list": [
            {
                "group_id": 7,
                "owner_user_id": 0,
                "name": "test",
                "notice": "未有公告",
                "introduction": "inc in test",
                "create_time": "2019-03-07 08:35:59.762750"
            },
            {
                "group_id": 8,
                "owner_user_id": 0,
                "name": "test",
                "notice": "未有公告",
                "introduction": "inc in test",
                "create_time": "2019-03-07 08:43:06.604291"
            },
            {
                "group_id": 9,
                "owner_user_id": 0,
                "name": "test",
                "notice": "未有公告",
                "introduction": "inc in test",
                "create_time": "2019-03-07 08:45:28.999273"
            },
            {
                "group_id": 10,
                "owner_user_id": 0,
                "name": "test",
                "notice": "未有公告",
                "introduction": "inc in test",
                "create_time": "2019-03-07 08:47:43.219607"
            },
            {
                "group_id": 11,
                "owner_user_id": 0,
                "name": "test",
                "notice": "未有公告",
                "introduction": "inc in test",
                "create_time": "2019-03-07 16:49:59.232931"
            },
            {
                "group_id": 12,
                "owner_user_id": 123,
                "name": "",
                "notice": "未有公告",
                "introduction": "",
                "create_time": "2019-03-08 18:20:38.637201"
            },
            {
                "group_id": 13,
                "owner_user_id": 123,
                "name": "Airy is so cool",
                "notice": "未有公告",
                "introduction": "Airy intro \bis very long",
                "create_time": "2019-03-10 15:57:42.780649"
            },
            {
                "group_id": 14,
                "owner_user_id": 123,
                "name": "Airy is so cool2",
                "notice": "未有公告",
                "introduction": "Airy intro is very long2",
                "create_time": "2019-03-10 16:00:01.287017"
            }
        ]
    }
}        
```
* 查看关注的群组
    * path('indexFollow', QueryController.index_follow),
* 查看群组的成员
    * path('memberIndex/', QueryController.member_index),
* 查看群组（已测试
  * path('baseInfo/', QueryController.base_info),
* 查看群组内的活动
    * path('baseActivityIndex', QueryController.base_info_activity_index),
### Interactive
* 关注/取消关注群组
    * path('follow/', InteractiveController.follow),
    * path('disFollow/', InteractiveController.dis_follow)
  
    
