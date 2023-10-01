<div align="center">
  <a href="#"><img src="https://kiramibot.dev/img/logo.svg" width="180" height="180" alt="KiramiBotPluginLogo"></a>
</div>

<div align="center">

# kirami-plugin-sentry

_✨在 Sentry.io 上进行 KiramiBot 服务日志查看、错误处理 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/KomoriDev/kirami-plugin-sentry.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/kiramibot-plugin-sentry">
    <img src="https://img.shields.io/pypi/v/kirami-plugin-sentry.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

在 Sentry.io 上进行 KiramiBot 服务日志查看、错误处理，以及群聊消息提醒

## 💿 安装

在 KiramiBot 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install kirami-plugin-sentry
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add kirami-plugin-sentry
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add kirami-plugin-sentry
```

</details>
<details>
<summary>conda</summary>

```bash
conda install kirami-plugin-sentry
```

</details>

打开 KiramiBot 项目根目录下的配置文件, 以 `kirami.toml` 为例，在 `[plugin]` 部分追加写入

```toml
plugins = ["kiramit_plugin_sentry"]
```

## ⚙️ 配置

在 KiramiBot 项目的配置文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| sentry_dsn | 是 | 无 | [Sentry Docs](https://docs.sentry.io/platforms/python/configuration/options/) |
| sentry_environment | 否 | None | [Sentry Docs](https://docs.sentry.io/platforms/python/configuration/options/) |
| sentry_default_integrations | 否 | False | [sentry-python #653](https://github.com/getsentry/sentry-python/issues/653) |

## 🎉 使用

填写必须配置项 `sentry_dsn` ，即刻开始 sentry 之旅！

### 指令表

本插件提供了一个 [仅SUPERUSERS能使用的命令](./kirami_plugin_sentry/plugin.py)。可以用来快捷查看错误信息

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 追踪 | 主人 | 否 | 当前会话 | 回复报错消息 |
| 追踪 | 主人 | 否 | 私聊/群聊 | 追踪 <msg_id> |

> <msg_id> 代表这是一个**必填的参数**，即用 `<` 与 `>` 包裹的文本。

### 效果图

理论上，这里应该有几张效果图

~~如果你觉得这个插件很赞, 欢迎返图!~~

## 📄 许可证
本项目使用 [MIT](LICENSE) 许可证开源

```txt
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
