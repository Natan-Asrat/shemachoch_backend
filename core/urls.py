from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('oil_stock', views.OilStock)
router.register('sugar_stock', views.SugarStock)
router.register('distribute', views.DistributeAPI)
router.register('members', views.MemberAPI)
router.register('add_member', views.AddMemberAPI)

router.register('user', views.GetUser)

urlpatterns = [
    path('', include(router.urls)),
    path('download_csv', views.download_csv)
]