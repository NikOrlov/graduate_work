import asyncio
from db.postgres import async_session, DbService
from models.base import UserSubscriptions
from services.billing import get_billing_service
from core.config import settings


async def auto_prolongate_subscriptions(billing_service):
    async with async_session() as session:
        db_service = DbService(db=session)
        subscriptions = await db_service.select(
            UserSubscriptions,
            [(UserSubscriptions.auto_prolongate, True), (UserSubscriptions.is_active, True)]
        )

        for subscription in subscriptions:
            try:
                result = await billing_service.prolongate_subscribe(
                    user_id=subscription.user_id,
                    user_subscription_id=subscription.id
                )
                if result:
                    print(f"Subscription {subscription.id} prolonged successfully.")
                else:
                    print(f"Failed to prolong subscription {subscription.id}.")
            except Exception as e:
                print(f"Error prolonging subscription {subscription.id}: {str(e)}")


async def worker():
    billing_service = get_billing_service()
    while True:
        await auto_prolongate_subscriptions(billing_service)
        await asyncio.sleep(settings.auto_prolongate_check)  # Sleep for a day
