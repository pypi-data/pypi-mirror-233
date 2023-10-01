from kirami import on_command
from kirami.database import Argot
from kirami.matcher import Matcher
from kirami.depends import CommandArg
from kirami.permission import SUPERUSER


@on_command("追踪", "track", argot=True, permission=SUPERUSER)
async def get_error_by_argot(matcher: Matcher):
    plugin = matcher.get_argot("plugin")
    module = matcher.get_argot("module")
    event = matcher.get_argot("event")
    error = matcher.get_argot("error")

    msg = f"""
    插件：{plugin}
    模块：{module}
    事件：{event}

    错误信息：{error}
    """
    await matcher.finish(msg)


@on_command("追踪", "track", permission=SUPERUSER)
async def get_error_by_message(matcher: Matcher, msg_id: CommandArg):
    argot = await Argot.find(Argot.msg_id == int(msg_id.extract_plain_text())).get()
    if argot:
        info = argot.content
        plugin = info["plugin"]
        module = info["module"]
        event = info["event"]
        error = info["error"]
        msg = f"""
        插件：{plugin}
        模块：{module}
        事件：{event}
        错误信息：{error}
        """
    else:
        msg = "未找到对应ID的信息"
    await matcher.finish(msg)
