# Stripe Django Store

Django бэкенд с интеграцией Stripe API для обработки платежей. Поддерживает одиночные товары и заказы со скидками и налогами.

##  Функционал

### Данные от админки
login: kirill  
password: kirill
###  Обязательные требования
- Модель Item с полями: name, description, price
- API метод `GET /buy/{id}` - получение Stripe Session Id
- API метод `GET /item/{id}` - HTML страница товара с кнопкой Buy
- Интеграция с Stripe Checkout

###  Бонусные задачи
- [x] Docker контейнеризация
- [x] Environment variables
- [x] Django Admin панель
- [x] Публичный доступ для тестирования
- [x] Модель Order с объединением нескольких Item
- [x] Модели Discount и Tax


##  Технологии

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Payments**: Stripe API
- **Container**: Docker, Docker Compose
- **Deployment**: Пример для production
