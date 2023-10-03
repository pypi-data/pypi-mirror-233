<div align="center">
  <a href="#"><img src="https://kiramibot.dev/img/logo.svg" width="180" height="180" alt="KiramiBotPluginLogo"></a>
</div>

<div align="center">

# kirami-plugin-boardgame

_✨ 棋类游戏 五子棋、围棋、黑白棋 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/FrostN0v0/kirami-plugin-boardgame.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/kirami-plugin-boardgame">
    <img src="https://img.shields.io/pypi/v/kirami-plugin-boardgame.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>


## 📖 介绍

棋类游戏插件，包含五子棋、围棋、黑白棋。

抄自隔壁[nonebot-plugin-boardgame](https://github.com/noneplugin/nonebot-plugin-boardgame)

## 💿 安装

在 KiramiBot 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>
  
```bash
pip install kirami-plugin-boardgame
```
</details>
<details>
<summary>pdm</summary>

```bash
pdm add kirami-plugin-boardgame
```
</details>
<details>
<summary>poetry</summary>

```bash
poetry add kirami-plugin-boardgame
```
</details>
<details>
<summary>conda</summary>

```bash
conda install kirami-plugin-boardgame
```
</details>

打开 KiramiBot 项目根目录下的配置文件, 以 `kirami.toml` 为例，在 `[plugin]` 部分追加写入
```toml
plugins = ["kiramit_plugin_boardgame"]
```

## 🎉 使用
### 指令表
|       指令       | 权限  | 需要@ | 范围  |      说明       |
|:--------------:|:---:|:---:|:---:|:-------------:|
|   围棋/五子棋/黑白棋   | 群员  |  是  | 群聊  |   开启一局棋类游戏    |
|    落子 字母+数字    | 群员  |  否  | 群聊  |    如：落子 A1    |
|      停止下棋      | 群员  |  否  | 群聊  |    停止一局游戏     |
|      查看棋盘      | 群员  |  否  | 群聊  |    查看当前棋盘     |
|      跳过回合      | 群员  |  否  | 群聊  | 黑白棋规则下，跳过你的回合 |
|       悔棋       | 群员  |  否  | 群聊  |      悔棋       |
| 重载五子棋/围棋/黑白棋棋局 | 群员  |  否  | 群聊  | 继续群内已停止的棋局下棋  |

