from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # 自定义权限,判断用户删除收藏的时候是否是当前用户,obj代表传过来的models
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 返回models里面的user对象跟request.user对象对比是否是一个用户
        return obj.user == request.user