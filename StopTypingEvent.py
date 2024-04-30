

import attrs
from hikari import Snowflake
from hikari.traits import RESTAware
from hikari.events.base_events import Event


@attrs.define()
class StopTypingEvent(Event):
    app: RESTAware = attrs.field()
    user: Snowflake = attrs.field()
