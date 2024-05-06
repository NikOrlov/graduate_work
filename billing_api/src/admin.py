import http
import httpx
import logging

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from models.base import Subscriptions, Payments, UserSubscriptions
from core.config import settings

logger = logging.getLogger("billing_api")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        payload = {"username": form["username"], "password": form["password"]}
        auth_url = settings.auth_api_login_url

        async with httpx.AsyncClient() as client:
            response = await client.post(auth_url, data=payload, follow_redirects=True)

            if response.status_code != http.HTTPStatus.OK:
                logger.info("Invalid username or password")
                return False
            data = response.json()
            if "admin" not in data.get("roles"):
                logger.info("Admin role is missing")
                return False
            request.session.update({"token": data.get("access_token")})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True


class SubscriptionAdmin(ModelView, model=Subscriptions):
    column_list = [
        Subscriptions.id,
        Subscriptions.title,
        Subscriptions.price,
        Subscriptions.duration,
    ]
    column_details_list = [
        Subscriptions.id,
        Subscriptions.title,
        Subscriptions.price,
        Subscriptions.duration,
    ]
    column_formatters_detail = {
        Subscriptions.duration: lambda m, a: str(m.duration) + " month."
    }
    column_formatters = {
        Subscriptions.duration: lambda m, a: str(m.duration) + " month."
    }
    name_plural = "Subscriptions"
    column_searchable_list = [Subscriptions.title, Subscriptions.price]
    column_sortable_list = [
        Subscriptions.title,
        Subscriptions.price,
        Subscriptions.duration,
    ]
    icon = "fa-solid fa-medal"
    form_columns = [Subscriptions.title, Subscriptions.price, Subscriptions.duration]


class PaymentsAdmin(ModelView, model=Payments):
    column_list = [
        Payments.id,
        Payments.user_id,
        Payments.date_create,
        Payments.subscription,
        Payments.status,
    ]
    column_formatters = {
        Payments.subscription: lambda m, a: (
            m.subscription.title if m.subscription else None
        )
    }
    column_details_list = [
        Payments.id,
        Payments.user_id,
        Payments.date_create,
        Payments.status,
        Payments.subscription,
    ]
    name_plural = "Payments"
    icon = "fa-solid fa-wallet"
    column_searchable_list = [Payments.date_create, Payments.subscription_id]
    column_sortable_list = [
        Payments.date_create,
        Payments.subscription_id,
        Payments.status,
    ]
    form_columns = [Payments.user_id, "subscription", Payments.status]
    form_ajax_refs = {"subscription": {"fields": (Subscriptions.title,)}}


class UserSubscriptionsAdmin(ModelView, model=UserSubscriptions):
    column_list = [
        UserSubscriptions.id,
        UserSubscriptions.user_id,
        UserSubscriptions.subscription,
        UserSubscriptions.is_active,
        UserSubscriptions.auto_prolongate,
        UserSubscriptions.expiration_time,
        UserSubscriptions.payment,
    ]
    column_details_exclude_list = [
        UserSubscriptions.subscription_id,
        UserSubscriptions.payment_id,
    ]
    name_plural = "User Subscriptions"
    icon = "fa-solid fa-user-plus"
    column_searchable_list = [
        UserSubscriptions.user_id,
        UserSubscriptions.subscription_id,
    ]
    column_sortable_list = [
        UserSubscriptions.user_id,
        UserSubscriptions.subscription_id,
    ]
