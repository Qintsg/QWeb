# 用户模块表结构设计

> 本文档是 QWeb 用户、认证、第三方登录与账号扩展表的设计基线。当前实现采用早期开发迁移重置策略：不保留旧 UUID 用户数据，`accounts.User` 主键改为从 1 递增的 `uid BIGINT`。

## 实现约束

- Django `AUTH_USER_MODEL` 继续指向 `accounts.User`。
- `users.uid` 是后端用户主键和其他用户相关表外键；公开展示 ID 后续另行设计 `public_id` 或 `display_id`。
- Django 认证字段 `password`、`last_login`、`is_active`、`is_staff`、`is_superuser`、`groups`、`user_permissions` 仍保留在 `accounts.User` 上，以兼容 Django Admin、认证后端和 SimpleJWT。
- SimpleJWT 使用 `USER_ID_FIELD = "uid"`，token claim 仍为 `user_id`。
- 邮箱与手机号只保存在 `user_contact`，登录服务通过用户名、邮箱或手机号解析用户。
- 第三方账号首次登录不按邮箱自动绑定已有账号；即使邮箱相同，也必须让用户登录已有账号后确认绑定。
- 当前接线 provider 只有 GitHub；表结构、接口和 service 按 provider 扩展设计，不创建未实现平台入口。

## 0.账号注册与第三方登录规则说明

### 0.1 UID规则

|字段|规则|
|---|---|
|`uid`|系统在用户注册完成后自动生成|
|生成方式|从`1`开始顺序递增|
|用途|作为用户主键，以及其他用户相关表的外键|
|类型建议|`BIGINT`|
|是否可修改|不可修改|

说明：

- `uid`是系统内部用户唯一标识。
- 不建议把`uid`直接暴露给前端作为公开用户编号。
- 如果需要公开展示用户ID，建议额外设计`public_id`、`display_id`或用户主页短ID。

---

### 0.2 用户名规则

|规则项|说明|
|---|---|
|字段名|`username`|
|允许字符|英文字母`a-z`、`A-Z`、数字`0-9`、短横线`-`、下划线`_`、点号`.`|
|长度|3-32位|
|唯一性|唯一|
|大小写|不区分大小写|
|是否可登录|可以使用用户名登录|
|是否可修改|可修改|
|展示用途|可作为用户主页路径、登录名、唯一用户标识|

不允许：

|限制|示例|
|---|---|
|不能以特殊字符开头|`.qintsg`、`-qintsg`、`_qintsg`|
|不能以特殊字符结尾|`qintsg.`、`qintsg-`、`qintsg_`|
|不能连续使用特殊字符|`qintsg..dev`、`qintsg__dev`、`qintsg--dev`|
|不能包含空格|`qin tsg`|
|不能包含其他特殊符号|`@`、`#`、`$`、`%`、`^`、`&`、`*`、`/`、`\`、`?`|
|不能使用敏感词、保留词|`admin`、`root`、`system`|

推荐校验逻辑：

|校验项|规则|
|---|---|
|字符集合|只允许`a-z`、`A-Z`、`0-9`、`-`、`_`、`.`|
|长度|3-32|
|首尾字符|必须是字母或数字|
|连续特殊字符|不允许连续出现`.`、`-`、`_`中的任意特殊字符|
|唯一性|大小写不敏感唯一|
|保留词|命中保留词则拒绝|

---

### 0.3 昵称规则

|字段|规则|
|---|---|
|字段名|`nickname`|
|唯一性|可重复|
|字符范围|支持大部分字符|
|大小写|区分大小写|
|是否可登录|不可作为登录凭据|
|是否可修改|可修改|
|用途|页面展示名称|

说明：

- `nickname`只用于展示。
- `nickname`允许重复，因此不能作为用户唯一标识。
- 第三方登录自动注册时，优先使用第三方平台返回的显示名称作为`nickname`。

---

### 0.4 第三方登录流程

当用户使用第三方登录时，系统按照以下规则处理。

#### 情况一：已存在第三方账号关联

如果`user_oauth_accounts`中已存在对应记录：

|判断条件|处理方式|
|---|---|
|`provider`匹配|第三方平台一致|
|`provider_account_id`匹配|第三方平台用户ID一致|
|结果|直接登录对应用户|

---

#### 情况二：没有已关联账号

如果没有找到已关联的第三方账号，系统需要先询问用户：

> 是否绑定到已有账号？

用户有两个选择：

|选择|处理方式|
|---|---|
|绑定已有账号|要求用户先登录已有账号，然后将第三方账号绑定到该账号|
|不绑定已有账号|系统自动注册一个新账号，并绑定第三方账号|

---

#### 情况三：绑定到已有账号

如果用户选择绑定已有账号：

|步骤|说明|
|---|---|
|1|用户需要先通过用户名、邮箱、手机号或其他方式登录已有账号|
|2|登录成功后，系统将第三方账号写入`user_oauth_accounts`|
|3|后续再次使用该第三方账号登录时，直接进入已绑定账号|

安全要求：

- 绑定前必须验证用户对已有账号的控制权。
- 不能仅凭第三方邮箱相同就自动绑定到已有账号。
- 如果第三方邮箱和已有账号邮箱相同，可以提示用户绑定，但仍需要登录已有账号确认。

---

#### 情况四：不绑定，自动注册账号

如果用户选择不绑定已有账号，则系统自动创建新账号。

自动注册字段规则如下：

|字段|来源|处理规则|
|---|---|---|
|`uid`|系统生成|注册完成后自动生成，从1开始顺序递增|
|`username`|第三方平台用户名|优先使用第三方返回的用户名|
|`nickname`|第三方平台显示名称|使用第三方名称|
|`avatar_url`|第三方平台头像|如果第三方提供头像，则使用第三方头像|
|`password_hash`|空|第三方自动注册用户默认无密码|
|`email`|第三方平台邮箱|如果第三方返回邮箱，可写入`user_contact.email`|
|`email_verified_at`|第三方邮箱验证状态|如果第三方明确返回已验证，可记录验证时间|
|`user_oauth_accounts`|第三方账号信息|创建第三方账号绑定记录|

---

### 0.5 第三方用户名处理规则

第三方登录自动注册时，`username`优先使用第三方平台返回的用户名，但必须经过本系统用户名规则校验。

|情况|处理方式|
|---|---|
|第三方用户名存在，且符合规则，且未被占用|直接作为`username`|
|第三方用户名存在，但不符合规则|询问用户手动设置用户名|
|第三方用户名存在，但已被占用|询问用户手动设置用户名|
|第三方没有返回用户名|询问用户手动设置用户名|

说明：

- 第三方平台的`nickname`可以直接作为本系统`nickname`。
- 第三方平台的`username`不能无条件作为本系统`username`。
- 因为本系统`username`需要满足唯一性、格式规则和保留词限制。

---

## 1.`users`用户核心表

|字段名|类型|约束|说明|
|---|---|---|---|
|`uid`|`BIGINT`|主键、自增|用户唯一ID，从1开始顺序生成|
|`username`|`VARCHAR(32)`|唯一、非空、大小写不敏感唯一约束|用户名，可用于登录|
|`nickname`|`VARCHAR(64)`|可空|展示昵称，可重复，不可用于登录|
|`avatar_url`|`TEXT`|可空|头像URL|
|`password`|`VARCHAR(128)`|Django认证字段|Django密码哈希，第三方自动注册账号为不可用密码|
|`last_login`|`TIMESTAMPTZ`|可空|Django最后登录时间|
|`is_active`|`BOOLEAN`|非空，默认`true`|Django认证启用标记|
|`is_staff`|`BOOLEAN`|非空，默认`false`|Django Admin 访问标记|
|`is_superuser`|`BOOLEAN`|非空，默认`false`|Django 超级权限标记|
|`status`|`VARCHAR(32)`|非空，默认`active`|账号状态|
|`user_type`|`VARCHAR(32)`|非空，默认`normal`|用户类型|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|
|`deleted_at`|`TIMESTAMPTZ`|可空|软删除时间|

### 推荐枚举值

|字段|可选值|
|---|---|
|`status`|`active`、`inactive`、`banned`、`deleted`、`pending`|
|`user_type`|`normal`、`admin`、`system`|

---

## 2.`user_security`用户安全表

一对一关联`users`，主键为`uid`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`uid`|`BIGINT`|主键、外键|关联`users.uid`|
|`password_hash`|`TEXT`|可空|密码哈希快照，第三方登录自动注册用户可为空|
|`password_algo`|`VARCHAR(32)`|可空，默认`django`|密码算法|
|`password_updated_at`|`TIMESTAMPTZ`|可空|密码更新时间|
|`two_factor_enabled`|`BOOLEAN`|非空，默认`false`|是否开启二次验证|
|`two_factor_secret_enc`|`TEXT`|可空|加密后的2FA密钥|
|`failed_login_attempts`|`INT`|非空，默认`0`|连续登录失败次数|
|`locked_until`|`TIMESTAMPTZ`|可空|账号锁定到期时间|
|`last_login_at`|`TIMESTAMPTZ`|可空|最后登录时间|
|`last_login_ip`|`INET`|可空|最后登录IP|
|`last_login_user_agent`|`TEXT`|可空|最后登录设备UA|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|

说明：

- `password_hash`允许为空，用于支持纯第三方登录账号。
- 如果用户后续设置密码，再写入`password_hash`和`password_updated_at`。
- 不保存明文密码。

---

## 3.`user_contact`用户联系方式表

一对一关联`users`，主键为`uid`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`uid`|`BIGINT`|主键、外键|关联`users.uid`|
|`email`|`VARCHAR(254)`|大小写不敏感唯一、可空|邮箱|
|`phone`|`VARCHAR(32)`|唯一、可空|手机号|
|`email_verified_at`|`TIMESTAMPTZ`|可空|邮箱验证时间|
|`phone_verified_at`|`TIMESTAMPTZ`|可空|手机号验证时间|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|

说明：

- 第三方登录返回邮箱时，可以写入`email`。
- 只有第三方平台明确返回邮箱已验证时，才建议写入`email_verified_at`。
- 邮箱相同不代表一定是同一用户，不能直接自动绑定已有账号。

---

## 4.`user_profile`用户资料表

一对一关联`users`，主键为`uid`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`uid`|`BIGINT`|主键、外键|关联`users.uid`|
|`real_name`|`VARCHAR(64)`|可空|真实姓名|
|`gender`|`VARCHAR(16)`|可空|性别|
|`birthday`|`DATE`|可空|生日|
|`bio`|`TEXT`|可空|个人简介|
|`country`|`VARCHAR(64)`|可空|国家|
|`province`|`VARCHAR(64)`|可空|省份|
|`city`|`VARCHAR(64)`|可空|城市|
|`website`|`TEXT`|可空|个人网站|
|`github`|`TEXT`|可空|GitHub主页|
|`extra`|`JSONB`|非空，默认空对象|扩展资料|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|

### 推荐枚举值

|字段|可选值|
|---|---|
|`gender`|`male`、`female`、`other`、`unknown`|

---

## 5.`user_settings`用户设置表

一对一关联`users`，主键为`uid`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`uid`|`BIGINT`|主键、外键|关联`users.uid`|
|`language`|`VARCHAR(32)`|非空，默认`zh-CN`|语言偏好|
|`timezone`|`VARCHAR(64)`|非空，默认`Asia/Shanghai`|时区|
|`theme`|`VARCHAR(32)`|非空，默认`system`|主题|
|`notification_settings`|`JSONB`|非空，默认空对象|通知设置|
|`privacy_settings`|`JSONB`|非空，默认空对象|隐私设置|
|`preferences`|`JSONB`|非空，默认空对象|其他偏好设置|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|

### 推荐枚举值

|字段|可选值|
|---|---|
|`theme`|`light`、`dark`、`system`|

---

## 6.`user_oauth_accounts`第三方账号关联表

一对多关联`users`。该表不建议以`uid`作为唯一主键，因为一个用户可能绑定多个第三方账号。

|字段名|类型|约束|说明|
|---|---|---|---|
|`id`|`BIGINT`|主键、自增|第三方账号绑定记录ID|
|`uid`|`BIGINT`|外键、非空|关联`users.uid`|
|`provider`|`VARCHAR(64)`|非空|第三方平台|
|`provider_account_id`|`VARCHAR(255)`|非空|第三方平台用户ID|
|`provider_username`|`VARCHAR(255)`|可空|第三方平台用户名|
|`provider_nickname`|`VARCHAR(255)`|可空|第三方平台显示名称|
|`provider_email`|`VARCHAR(254)`|可空|第三方平台邮箱|
|`provider_email_verified`|`BOOLEAN`|可空|第三方平台邮箱是否已验证|
|`provider_avatar_url`|`TEXT`|可空|第三方平台头像|
|`access_token_enc`|`TEXT`|可空|加密后的访问令牌|
|`refresh_token_enc`|`TEXT`|可空|加密后的刷新令牌|
|`token_expires_at`|`TIMESTAMPTZ`|可空|令牌过期时间|
|`scopes`|`JSONB`|可空|授权范围|
|`raw_profile`|`JSONB`|非空，默认空对象|第三方原始用户信息|
|`linked_at`|`TIMESTAMPTZ`|非空|绑定时间|
|`updated_at`|`TIMESTAMPTZ`|非空|更新时间|

### 推荐唯一约束

|约束|说明|
|---|---|
|`UNIQUE(provider,provider_account_id)`|防止同一个第三方账号绑定到多个用户|
|`UNIQUE(uid,provider)`|当前实现限制每个用户每个平台只能绑定一个账号|

说明：

- 如果允许一个用户绑定多个同平台账号，例如多个GitHub账号，就不要使用`UNIQUE(uid,provider)`。
- `provider_account_id`必须使用第三方平台稳定唯一ID，不建议使用第三方用户名。
- 第三方用户名可能会变更，不能作为第三方账号唯一标识。

---

## 7.`user_login_logs`用户登录日志表

一对多关联`users`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`id`|`BIGINT`|主键、自增|日志ID|
|`uid`|`BIGINT`|外键、可空|关联`users.uid`|
|`login_type`|`VARCHAR(32)`|非空|登录方式|
|`provider`|`VARCHAR(64)`|可空|第三方平台|
|`ip`|`INET`|可空|登录IP|
|`user_agent`|`TEXT`|可空|浏览器或客户端UA|
|`device_info`|`JSONB`|非空，默认空对象|设备信息|
|`success`|`BOOLEAN`|非空|是否登录成功|
|`failure_reason`|`TEXT`|可空|失败原因|
|`created_at`|`TIMESTAMPTZ`|非空|日志创建时间|

### 推荐枚举值

|字段|可选值|
|---|---|
|`login_type`|`password`、`oauth`、`sms`、`email_code`、`token`|

---

## 8.`user_refresh_tokens`刷新令牌表

适合JWT登录体系，一对多关联`users`。

|字段名|类型|约束|说明|
|---|---|---|---|
|`id`|`BIGINT`|主键、自增|令牌记录ID|
|`uid`|`BIGINT`|外键、非空|关联`users.uid`|
|`token_hash`|`TEXT`|唯一、非空|刷新令牌哈希|
|`device_id`|`VARCHAR(128)`|可空|设备ID|
|`device_name`|`VARCHAR(128)`|可空|设备名称|
|`ip`|`INET`|可空|签发IP|
|`user_agent`|`TEXT`|可空|客户端UA|
|`expires_at`|`TIMESTAMPTZ`|非空|过期时间|
|`revoked_at`|`TIMESTAMPTZ`|可空|吊销时间|
|`created_at`|`TIMESTAMPTZ`|非空|创建时间|

---

## 9.用户名变更建议

由于`username`允许修改，建议后续根据业务需要增加用户名变更限制。

|规则|规则内容|
|---|---|
|修改频率|限制为每30天修改一次|
|唯一性|修改时重新检查大小写不敏感唯一|
|保留词|修改时重新检查敏感词和保留词|
|历史记录|防止他人抢注旧用户名，增加用户名历史表（自行设计）|
|登录影响|修改用户名后，原用户名不再可用于登录|

扩展表：

|表名|用途|
|---|---|
|`user_username_history`|记录用户名修改历史|
|`user_reserved_names`|维护保留词、敏感词、系统占用名|

---

## 10.总体关系

|表名|关系|主键|说明|
|---|---|---|---|
|`users`|主表|`uid`|用户核心账号|
|`user_security`|一对一|`uid`|用户安全信息|
|`user_contact`|一对一|`uid`|邮箱、手机号|
|`user_profile`|一对一|`uid`|用户资料|
|`user_settings`|一对一|`uid`|用户偏好设置|
|`user_oauth_accounts`|一对多|`id`|第三方账号绑定|
|`user_login_logs`|一对多|`id`|登录日志|
|`user_refresh_tokens`|一对多|`id`|刷新令牌|
