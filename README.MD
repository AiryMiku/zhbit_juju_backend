# zhbit_juju_backend

# request_key_dict 规定
```json
{
  "[request_param_key]": "validate_rule" 
}
```

# 标准返回格式
```json
{
  "code": 0,
  "data": {
    ...
  }
}
```

## 群组
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
* 查看所有活动（已测试
  * path('indexAll/', QueryController.index),
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
  
    