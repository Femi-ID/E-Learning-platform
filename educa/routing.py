from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
# ProtocolTypeRouter- maps HTTP requests to the standard Django views if no  http mapping is provided
# URLRouter- maps websocket connections URL patterns in the 'websocket_urlpatterns'

# AuthMiddlewareStack- supports standard Django authentication, where the user details are stored in the session.
# Access the user instance in the scope of the consumer to identify the user who sends a message.

