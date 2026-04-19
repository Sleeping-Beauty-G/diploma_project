from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_order_email_task(self, email, order_id):
    send_mail(
        subject="Order confirmed",
        message=f"Ваш заказ #{order_id} успешно оформлен",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )