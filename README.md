# 纸短情长（EL）

> 一个基于 Flask 的书信叙事网页小游戏：在四个场景中与 NPC 对话，写下、投递、拾取和回复信件，用一封封信拼出属于自己的故事。

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [游戏场景](#游戏场景)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [接口一览](#接口一览)
- [打包为可执行文件](#打包为可执行文件)
- [配置说明](#配置说明)
- [许可证](#许可证)

---

## 项目简介

《纸短情长》是一个以「写信」为核心交互的剧情向网页游戏。玩家注册登录后进入四个主题场景，
每个场景配有独立的背景、背景音乐与 NPC 对话剧情。玩家可以：

- **写信**：把想说的话写成信，署上名字，选择情绪标签，并决定是否公开自己的身份；
- **投递 / 拾取**：未指定收信人的信会留在当前场景中，被其他玩家**拾取**阅读；
- **回复**：读到别人的信后可以直接回信，形成一来一回的书信往来；
- **读信**：随时查看自己「写过的」「收到的」「读过的」信件，未读信件带红点提醒。

后端使用 Flask + SQLAlchemy 持久化用户与信件数据，前端为原生 HTML/CSS/JavaScript，
通过 `fetch` 异步调用接口，实现对话推进、场景切换、信件弹窗等交互。

## 功能特性

- **用户系统**：注册 / 登录 / 登出，基于 Flask-WTF 表单校验与 session 会话，密码校验后写入 session。
- **书信系统**：写信、回信、拾取、已读标记；信件按「我写的 / 我收到的 / 我读过的」三类归档。
- **情绪标签**：写信时可标注 `happy` / `sad` / `suggestion`，在信件列表中以色块区分。
- **匿名投递**：`Is_show_writer` 控制是否向读者公开写信人身份。
- **场景系统**：四个场景各自绑定背景图与背景音乐，切换场景时动态更换 `bg-music` 音源。
- **NPC 对话引擎**：`NPC` 类支持多段对话、状态机（`state` / `next_index`）、分支选项，并预留了 `ai_api` 字段用于接入外部 AI 对话接口。
- **免数据库初始化**：首次运行自动建表，无需手动执行迁移。

## 游戏场景

| # | 场景 | 主题 |
|---|------|------|
| 1 | 寻找真我 | 在迷茫中辨认自己的声音 |
| 2 | 爱是成长的通项公式 | 关于亲密关系与成长 |
| 3 | 职场倒影与青春突围 | 理想与现实之间的拉扯 |
| 4 | 爷爷的话 | 来自长辈的叮咛与告别 |

<details>
<summary>点击展开场景预览图</summary>

| 寻找真我 | 爱是成长的通项公式 |
|---|---|
| ![](game/static/images/address1_bg.jpg) | ![](game/static/images/address2_bg.png) |

| 职场倒影与青春突围 | 爷爷的话 |
|---|---|
| ![](game/static/images/address3_bg.jpg) | ![](game/static/images/address4_bg.png) |

</details>

## 技术栈

| 层次 | 选型 |
|------|------|
| 后端框架 | Flask 3.1 |
| ORM | Flask-SQLAlchemy / SQLAlchemy 2.0 |
| 数据库 | SQLite（通过 `SQLALCHEMY_DATABASE_URI` 可替换） |
| 表单与校验 | Flask-WTF / WTForms |
| 数据库迁移 | Flask-Migrate（Alembic） |
| 前端 | 原生 HTML5 / CSS3 / JavaScript（`fetch` 异步请求） |
| 打包 | PyInstaller |

## 项目结构

```
EL_2/
├── run.py                  # 程序入口，启动开发服务器
├── run.spec                # PyInstaller 打包配置
├── config.py               # 应用配置（密钥、数据库 URI 等）
├── requirements.txt        # 运行依赖
├── game/                   # 应用包
│   ├── __init__.py         # create_app() 工厂、db/migrate 扩展初始化
│   ├── models/
│   │   ├── user.py         # User、Text(抽象基类)、Letter 数据模型
│   │   └── NPC.py          # NPC 对话引擎与 Map 场景数据（含剧本内容）
│   ├── routes/
│   │   ├── login.py        # 登录 / 注册 / 登出蓝图
│   │   └── play.py         # 主场景、读信、写信、拾信蓝图
│   ├── templates/          # index.html（登录注册页）、play.html（游戏主界面）
│   └── static/
│       ├── css/            # 页面样式
│       ├── js/             # async.js / dialog.js / help-func.js
│       ├── images/         # 场景背景、NPC 立绘、道具素材
│       └── music/          # 场景背景音乐与音效
└── instance/               # 运行时自动生成，存放 SQLite 数据库（已被 .gitignore 忽略）
```

## 快速开始

### 环境要求

- Python 3.9 及以上（开发环境为 3.13）
- pip

### 安装与运行

```bash
# 1. 克隆仓库
git clone https://github.com/lcdmiku/EL.git
cd EL

# 2. 创建并激活虚拟环境
python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS / Linux
source myenv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动
python run.py
```

启动后访问 <http://127.0.0.1:5000>，先**注册**一个账号，再登录进入游戏。

> 数据库文件在首次运行时自动创建于 `instance/test.db`，无需手动初始化。
> 如需重置游戏数据，直接删除该文件后重新启动即可。

## 接口一览

| 方法 | 路由 | 说明 |
|------|------|------|
| GET | `/` | 登录 / 注册页面 |
| POST | `/login` | 登录校验，成功返回跳转地址（JSON） |
| POST | `/register` | 注册新用户（JSON） |
| GET | `/logout` | 退出登录并清除 session |
| GET/POST | `/play` | 游戏主场景；POST 处理读信 / 写信 / 拾信 / 切换场景 |
| POST | `/read` | 按分类拉取当前用户的信件列表 |
| POST | `/write` | 写信或回信 |
| POST | `/collect` | 拾取当前场景中未被指定收信人的信件 |
| POST | `/Is_viewed` | 将信件标记为已读并记录阅读者 |

所有 POST 接口均受 Flask-WTF 的 CSRF 保护，前端在请求头中携带 `X-CSRFToken`。

## 打包为可执行文件

项目已提供 `run.spec`，安装 PyInstaller 后可直接打包：

```bash
pip install pyinstaller
pyinstaller run.spec
```

产物位于 `dist/run/`，双击 `run.exe` 即可运行。
打包配置会自动带上 `game/static` 与 `game/templates` 资源目录。

## 配置说明

配置集中在 `config.py`：

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| `DEBUG` | `True` | 调试模式 |
| `SECRET_KEY` | `'your_secret_key'` | **部署前请务必替换为随机密钥** |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///test.db` | 数据库连接串，可换成 MySQL / PostgreSQL |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | `True` | SQLAlchemy 变更追踪 |

> ⚠️ `SECRET_KEY` 用于签名 session 与 CSRF token。当前为占位值，正式部署时请改为随机字符串，
> 并通过环境变量注入，不要硬编码在代码里提交到仓库。

## 许可证

本项目采用 [MIT License](LICENSE)。
