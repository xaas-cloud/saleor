from collections.abc import Iterable
from functools import partial
from typing import Optional, Union

from ...account.models import User
from ...app.models import App
from ...product.models import Product
from ..event_types import WebhookEventAsyncType
from ..models import Webhook
from ..payloads import generate_product_payload
from ..utils import get_webhooks_for_event


def product_created(
    product: Product,
    requestor: Union[User, App],
    webhooks: Optional[Iterable[Webhook]] = None,
    allow_replica: bool = True,
):
    from ..transport.asynchronous import trigger_webhooks_async

    event_type = WebhookEventAsyncType.PRODUCT_CREATED

    if webhooks is None:
        webhooks = get_webhooks_for_event(event_type)

    if webhooks:
        product_data_generator = partial(generate_product_payload, product, requestor)
        trigger_webhooks_async(
            None,
            event_type,
            webhooks,
            product,
            requestor,
            legacy_data_generator=product_data_generator,
            allow_replica=allow_replica,
        )
