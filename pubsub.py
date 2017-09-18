"""This module provides a basic publisher/subscriber implementation.

Example:
    def foo(msg):
        print(msg)

    pubsub.subscribe('MESSAGE', foo)
    pubsub.publish('MESSAGE', 'bar')
    pubsub.unsubscribe('MESSAGE', foo)

    >>> bar
"""

_events = {}


def subscribe(event, callback):
    """Subscribes to the given event.

    event: A string identifier.

    call: A function callback.
    """

    if event not in _events:
        _events[event] = []

    if callback not in _events[event]:
        _events[event].append(callback)


def unsubscribe(event, callback):
    """Unsubscribes to the given event.

    event: A string identifier.

    call: A function callback.

    Raises:
        ValueError: If event or callback not present.
    """

    subscribers = _events.get(event)

    if not subscribers:
        raise ValueError('pubsub.unsubscribe(e, x): no subscribers for e')

    if callback in subscribers:
        subscribers.remove(callback)

    else:
        raise ValueError('pubsub.unsubscribe(e, x): x not subscribed to e')


def publish(event, *args, **kwargs):
    """Publishes an event

    event: A string identifier.

    args: Callback args

    kwargs: Callback kwargs
    """

    subscribers = _events.get(event)

    for sub in subscribers:
        sub(*args, **kwargs)
