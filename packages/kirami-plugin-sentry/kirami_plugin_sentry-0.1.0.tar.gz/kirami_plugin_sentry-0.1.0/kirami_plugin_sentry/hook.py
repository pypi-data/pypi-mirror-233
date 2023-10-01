from kirami.hook import after_run
from kirami.database import Argot
from kirami.typing import Event, Matcher


@after_run
async def alert(event: Event, matcher: Matcher, exception: Exception | None):
    if not exception:
        return

    error = exception.__class__.__name__ + ": " + str(exception)

    msg = f"指令在处理过程中发生了出乎意料的错误，请联系超管：\n{error}"

    message = await matcher.send(msg)
    await Argot(
        msg_id=message["message_id"],
        content={
            "plugin": matcher.plugin_name,
            "module": str(matcher.module),
            "event": event.get_event_description(),
            "error": error,
        },
    ).save()
