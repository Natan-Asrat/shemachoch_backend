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
    path('download_oil_report', views.download_oil_csv),
    path('download_sugar_report', views.download_sugar_csv)
]