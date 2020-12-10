from rest_framework import permissions


class ReadOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user


class Moderator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # else:
        return True
            # даем право на любой http запрос к отзывам и комментам


# Администратор - IsAdminUser
# IsOwnerOrReadOnly
#     аноним
#     аутентифицированный




# аноним может читать отзывы и комменты
# аутентифицированный + публиковать ревью и комменты, ставить рейтинг
#     редактировать и удалять свои отзывы
# модератор + право рендкатировать и удалять любые отзывы и комменты
# админ - все правва
