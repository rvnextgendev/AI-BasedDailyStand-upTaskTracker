from typing import Any, Dict
from ..core.services import NotificationService
from ..schemas import SendNotificationInput, UserContext


def send_notification(args: Dict[str, Any], user: UserContext, svc: NotificationService) -> Dict[str, Any]:
    data = SendNotificationInput(**args)
    return svc.send(to=data.to, channel=data.channel, subject=data.subject, message=data.message)
