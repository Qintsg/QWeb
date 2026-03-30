# ADR-003: 存储策略决策

> 状态: **已采纳**  
> 日期: 2025

---

## 背景

QWeb 中多个模块需要文件存储能力：媒体中心、博客附图、文件存储、临时传输。需要在项目初期选择合适的存储方案，并预留未来升级路径。

## 决策

### 分阶段存储策略

**阶段 1（当前）: 本地文件存储**

```text
/data/
  ├── media/        # 媒体文件
  ├── uploads/      # 用户上传
  ├── temp/         # 临时传输
  └── backups/      # 备份
```

- Django `FileField` / `ImageField` 写入本地 `/data/` 挂载
- Nginx 直接提供静态文件服务
- 简单、零依赖、适合初期

**阶段 2（未来）: MinIO S3 兼容存储**

- 引入 MinIO 作为对象存储
- 使用 django-storages + boto3 切换存储后端
- 业务代码通过 media_center 抽象层访问，无需修改

### 搜索策略

**阶段 1**: PostgreSQL 全文搜索（`SearchVector` + `SearchRank`）  
**阶段 2**: Meilisearch 或 Elasticsearch（当数据量/需求增长时）

### 监控策略

**阶段 1**: Sentry 错误跟踪  
**阶段 2**: Prometheus + Grafana 指标监控  
**阶段 3**: Loki / ELK 日志聚合

## 理由

- **为什么不直接用 S3/MinIO？**  
  初期文件量小，本地存储零配置启动。通过抽象层保证切换无痛。

- **为什么不直接用 Elasticsearch？**  
  PostgreSQL 全文搜索对中等数据量够用。避免初期引入过多基础设施。

- **为什么分阶段？**  
  个人项目资源有限，先用最简单方案跑通，需求增长时再升级。架构设计预留了升级路径。

## 关键约束

- 所有文件操作必须通过 `media_center` 或 `storage` 模块的 service 层
- 禁止业务模块直接操作文件系统路径
- 文件元数据（文件名、大小、MIME、上传者、权限）存 PostgreSQL
- 文件内容存储路径由存储后端决定

## 替代方案

| 方案 | 评估 | 否决原因 |
|------|------|----------|
| 直接 S3 | 生产级 | 初期配置开销大 |
| 数据库 BLOB | 简单 | 性能差，不适合大文件 |
| NFS | 共享存储 | 单机部署无需网络文件系统 |

## 影响

- `media_center` 需要定义统一的文件存储 service 接口
- `storage` / `temp_transfer` 通过此接口存取文件
- 切换到 MinIO 时只需修改 Django settings 中的 `DEFAULT_FILE_STORAGE` 和 media_center 配置
- 文件清理策略需在 Celery 定时任务中实现
