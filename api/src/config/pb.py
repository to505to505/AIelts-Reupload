from pocketbase import PocketBase
import os

from .sheduler import scheduler

pb = PocketBase(os.getenv("POCKETBASE_URL"))
pb.collection("_superusers").auth_with_password(
    os.getenv("POCKETBASE_ADMIN_EMAIL"), os.getenv("POCKETBASE_ADMIN_PASSWORD")
)


@scheduler.scheduled_job("interval", hours=2)
def authenticate_pocketbase():
    """Функция для обновления аутентификации в PocketBase."""
    try:
        auth_response = pb.collection("_superusers").auth_refresh()
        print(
            "PocketBase authentication refreshed with",
            auth_response.token[:10],
            auth_response.record,
        )
        pb.auth_store.save(auth_response.token, auth_response.record)
    except Exception as e:
        print(f"Failed to refresh PocketBase authentication: {e}")
