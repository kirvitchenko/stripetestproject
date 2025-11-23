import stripe


def create_stripe_session(order):
    """
    Функция для реализации создания Stripe сессии
    1. Создаем stripe_tax_id для того чтобы применить его к каждому предмету в заказе
    2. Добавляем каждую позицию в заказа, применяем к ней налог
    3.Создаем словарь с параметрами сессии
    4. Если есть скидка, добавляес ее в параметры
    5. Создаем и возращаем сессию
    """
    line_items = []

    if order.tax:
        if not order.tax.stripe_tax_id:
            tax_rate = stripe.TaxRate.create(
                percentage=float(order.tax.tax_rate),
                inclusive=False,
                display_name=order.tax.name,
            )
            order.tax.stripe_tax_id = tax_rate.id
            order.tax.save()

    for order_item in order.order_items.all():
        line_item = {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": order_item.item.name,
                    "description": order_item.item.description,
                },
                "unit_amount": order_item.item.get_price_in_cents(),
            },
            "quantity": order_item.quantity,
        }

        if order.tax:
            line_item["tax_rates"] = [order.tax.stripe_tax_id]

        line_items.append(line_item)

    session_params = {
        "payment_method_types": ["card"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": "http://localhost:8000/success/",
        "cancel_url": "http://localhost:8000/cancel/",
    }
    if order.discount:
        if not order.discount.stripe_coupon_id:
            coupon = stripe.Coupon.create(
                percent_off=float(order.discount.discount_value),
                duration="once",
                name=order.discount.name,
            )
            order.discount.stripe_coupon_id = coupon.id
            order.discount.save()
        session_params["discounts"] = [{"coupon": order.discount.stripe_coupon_id}]

    session = stripe.checkout.Session.create(**session_params)
    return session
