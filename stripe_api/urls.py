from django.urls import path

from stripe_api.views import (
    ItemDetailView,
    SingleCheckoutSession,
    OrderCheckoutSession,
    OrderDetailView,
)

urlpatterns = [
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item"),
    path("buy/<int:pk>/", SingleCheckoutSession.as_view(), name="session"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("buy/order/<int:pk>/", OrderCheckoutSession.as_view(), name="buy_order"),
]
