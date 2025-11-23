from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import ForeignKey


class Item(models.Model):
    """Модель обьекта в магазине, содежит название, описание и цену за предмет"""
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.name

    def get_price_in_cents(self):
        """Функция для того чтобы сразу преобразоваться цену в соотвествующую требованиям Stripe"""
        return int(self.price * 100)


class Discount(models.Model):
    """Скидка в %"""
    name = models.CharField(max_length=200)
    discount_value = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MaxValueValidator(100)]
    )
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.discount_value}%"


class Tax(models.Model):
    """Налог в %"""
    name = models.CharField(max_length=200)
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MaxValueValidator(100)]
    )
    stripe_tax_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.tax_rate}%"


class Order(models.Model):
    """Модель заказа которая обьединяет в себе предметы, общую стоимость, налог и скидку"""
    items = models.ManyToManyField(Item, through="OrderItem", related_name="orders")
    total_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    discount = ForeignKey(Discount, on_delete=models.PROTECT, blank=True, null=True)
    tax = ForeignKey(Tax, on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Автоматически пересчитываем цену при сохранении"""
        self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self):
        """Вычисляет и сохраняет итоговую сумму"""
        base_total = sum(
            order_item.item.price * order_item.quantity
            for order_item in self.order_items.all()
        )
        total = base_total

        if self.discount:
            discount_amount = base_total * (self.discount.discount_value / 100)
            total -= discount_amount

        if self.tax:
            tax_amount = total * (self.tax.tax_rate / 100)
            total += tax_amount

        self.total_price = round(total, 2)


class OrderItem(models.Model):
    """Промежуточная таблица для связи заказа и предмета"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """При сохранении позиции пересчитываем сумму заказа"""
        super().save(*args, **kwargs)
        self.order.calculate_total()
