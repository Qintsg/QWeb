# 快速开始指南

> 面向新加入的开发者，快速搭建 QWeb 本地开发环境

---

## 1. 前置条件

| 工具 | 最低版本 | 安装确认 |
|------|----------|----------|
| Python | 3.13 | `python --version` |
| Node.js | 20 LTS | `node --version` |
| PostgreSQL | 16 | `psql --version` |
| Redis | 7 | `redis-cli ping` |
| Git | 2.40+ | `git --version` |

---

## 2. 克隆仓库

```bash
git clone <repo_url>
cd QWeb
```

---

## 3. 数据库初始化

```bash
# 使用项目提供的初始化脚本
psql -U postgres -v qweb_db=qweb -v qweb_user=qweb_app -v qweb_password='replace-with-local-password' -f docs/postgresql-init.sql
```

脚本将创建：
- 数据库: `qweb`
- 用户: 由执行脚本时的 `qweb_user` 变量指定
- 授予所有权限

---

## 4. 后端启动

```bash
cd backend

# 安装依赖
uv sync

# 复制环境变量（按需修改 DB 和 Redis 配置）
cp .env.example .env

# 数据库迁移
uv run python manage.py migrate

# 首次部署站长账号会在首次访问前端时引导创建；也可使用交互式命令创建
uv run python manage.py seed_admin

# 启动开发服务器
uv run python manage.py runserver 0.0.0.0:8000
```

如需启用 GitHub 登录，需要在 GitHub OAuth App 中配置回调地址：

```text
http://127.0.0.1:5173/auth/github/callback
```

并在 `backend/.env` 中填写：

```env
GITHUB_OAUTH_CLIENT_ID=your-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-client-secret
GITHUB_OAUTH_CALLBACK_URL=http://127.0.0.1:5173/auth/github/callback
```

前端通过 `/api/v1/auth/oauth/github/authorize/` 获取授权地址。首次 GitHub 登录未绑定本地账号时，会在回调页选择“绑定已有账号”或“创建新账号”；邮箱相同不会自动绑定。

验证后端是否运行：

| 地址 | 说明 |
|------|------|
| http://localhost:8000/api/health/ | 健康检查 |
| http://localhost:8000/api/docs/ | Swagger 文档 |
| http://localhost:8000/api/schema/ | OpenAPI Schema |

---

## 5. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 复制环境变量
cp .env.example .env

# 启动开发服务器
npm run dev
```

前端启动后访问：http://localhost:5173

---

## 6. 开发工具推荐

### IDE

- **VS Code** + 以下扩展：
  - Python (ms-python)
  - Pylance
  - Volar (Vue)
  - ESLint
  - Prettier
  - Django
  - Thunder Client（API 调试）

### 浏览器

- Vue DevTools 浏览器扩展
- Pinia DevTools

### 数据库

- pgAdmin 4 / DBeaver / DataGrip

---

## 7. 常用命令速查

### 后端

```bash
# 创建新 app
uv run python manage.py startapp <app_name> apps/<app_name>

# 生成迁移
uv run python manage.py makemigrations <app_name>

# 执行迁移
uv run python manage.py migrate

# Django Shell
uv run python manage.py shell

# 启动 Celery Worker
celery -A config worker -l info

# 启动 Celery Beat
celery -A config beat -l info

# 运行测试
uv run python manage.py test
# 或
pytest
```

### 前端

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 类型检查
npx vue-tsc --noEmit

# ESLint 检查
npm run lint
```

---

## 8. 项目结构速览

```text
QWeb/
├── backend/                      # Django 后端
│   ├── apps/                     # 业务模块（17 个 app）
│   │   ├── core/                 # 基础设施
│   │   ├── accounts/             # 用户认证
│   │   ├── iam/                  # 角色权限
│   │   ├── audit/                # 审计日志
│   │   ├── system_config/        # 系统配置
│   │   ├── notifications/        # 通知
│   │   ├── media_center/         # 媒体中心
│   │   ├── blog/                 # 博客
│   │   ├── wiki/                 # 知识库
│   │   ├── storage/              # 文件存储
│   │   ├── temp_transfer/        # 临时传输
│   │   ├── network_tools/        # 网络工具
│   │   ├── frp_manager/          # FRP 隧道
│   │   ├── ssh_gateway/          # SSH 网关
│   │   ├── mc_manager/           # MC 管理
│   │   ├── mail_center/          # 邮件中心
│   │   └── dev_workspace/        # 远程开发
│   ├── config/                   # Django 项目配置
│   ├── manage.py
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/                     # Vue 3 前端
│   ├── src/
│   │   ├── api/                  # API 接口
│   │   ├── components/           # 组件
│   │   ├── composables/          # 组合式函数
│   │   ├── layouts/              # 布局组件
│   │   ├── pages/                # 页面
│   │   ├── router/               # 路由
│   │   ├── stores/               # Pinia Store
│   │   ├── styles/               # 样式与 Token
│   │   ├── types/                # TypeScript 类型
│   │   └── utils/                # 工具函数
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
└── docs/                         # 项目文档
    ├── architecture/             # 架构设计
    ├── backend/                  # 后端开发
    ├── frontend/                 # 前端开发
    ├── workflow/                 # 工作流
    └── decisions/                # 架构决策记录
```

---

## 9. 下一步

环境搭建完成后，建议：

1. 阅读 [总体架构](../总体架构.md) 了解完整设计
2. 阅读 [模块边界](../architecture/module-boundaries.md) 了解各模块职责
3. 阅读 [开发工作流](./development-workflow.md) 了解开发规范
4. 阅读 [API 设计](../architecture/api-design.md) 了解接口契约
5. 按模块顺序开始开发
