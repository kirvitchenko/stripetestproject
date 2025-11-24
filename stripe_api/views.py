import stripe
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from stripe_api.models import Item, Order, OrderItem
from stripe_api.utils.stripe_session import create_stripe_session

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name='dispatch')
class ItemDetailView(APIView):
    """Представление одного предмета"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "stripe_api/item.html"

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return Response(
            {"item": item, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY},
        )

@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailView(APIView):
    """Представление заказа предметов"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "stripe_api/order.html"

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return Response(
            {"order": order, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}
        )

@method_decorator(csrf_exempt, name='dispatch')
class SingleCheckoutSession(APIView):
    """Если предмет один, под капотом делаем для него заказ и перенаправляем на форму Stripe"""
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        order = Order.objects.create()
        OrderItem.objects.create(item=item, order=order, quantity=1)

        session = create_stripe_session(order)
        return Response({"id": session.id})

@method_decorator(csrf_exempt, name='dispatch')
class OrderCheckoutSession(APIView):
    """Перенаправляем на форму заказа"""

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        session = create_stripe_session(order)
        return Response({"id": session.id})
