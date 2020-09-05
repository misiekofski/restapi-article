from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from restapi import views

router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'user', views.UserViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Drinking Day API",
      default_version='v1',
      description="This API allows us to keep a diary of our daily drinking",
      terms_of_service="https://www.scvconsultants.com",
      contact=openapi.Contact(email="michal@scvconsultants.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]