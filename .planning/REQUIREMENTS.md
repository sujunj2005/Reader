# Requirements

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: 用户可以使用邮箱和密码注册账户
- [ ] **AUTH-02**: 用户可以登录并保持跨会话登录状态
- [ ] **AUTH-03**: 用户可以从任何页面登出
- [ ] **AUTH-04**: 用户可以重置密码

### Content Management

- [ ] **CONT-01**: 管理员可以添加小说源（配置爬虫目标网站）
- [ ] **CONT-02**: 系统可以增量爬取小说内容（按网站规则定时更新）
- [ ] **CONT-03**: 用户可以手动触发特定源的爬取
- [ ] **CONT-04**: 系统可以导入本地小说文件（TXT、EPUB 等格式）
- [ ] **CONT-05**: 系统解析导入文件的元数据（标题、作者、章节）
- [ ] **CONT-06**: 管理员可以管理小说元数据（编辑、删除）

### Reading Experience

- [ ] **READ-01**: 用户可以在线阅读小说章节
- [ ] **READ-02**: 系统保存用户的阅读进度
- [ ] **READ-03**: 用户可以添加书签到特定章节
- [ ] **READ-04**: 用户可以调整阅读设置（字体大小、夜间模式）
- [ ] **READ-05**: 用户可以查看和访问历史记录

### Book Management

- [ ] **BOOK-01**: 用户可以搜索小说（按标题、作者）
- [ ] **BOOK-02**: 系统提供小说分类和标签浏览
- [ ] **BOOK-03**: 用户可以管理个人书架（添加/移除小说）
- [ ] **BOOK-04**: 系统显示小说详情（元数据、章节列表、翻译状态）

### Translation Module

- [ ] **TRANS-01**: 系统支持对接多种大模型（OpenAI、Claude、本地部署模型）
- [ ] **TRANS-02**: 用户可以选择翻译整本小说或单个章节
- [ ] **TRANS-03**: 用户可以配置翻译并发数
- [ ] **TRANS-04**: 系统管理翻译任务队列（开始、暂停、取消）
- [ ] **TRANS-05**: 系统保存翻译结果到本地源
- [ ] **TRANS-06**: 用户可以查看翻译进度和状态
- [ ] **TRANS-07**: 用户可以配置目标翻译语言

### Deployment

- [ ] **DEPLOY-01**: 所有服务可通过 Docker Compose 一键部署
- [ ] **DEPLOY-02**: 系统提供默认配置文件和环境变量模板
- [ ] **DEPLOY-03**: 系统支持配置不同的 AI 模型 API 密钥和端点

### User Profile

- [ ] **USER-01**: 用户可以查看和编辑个人资料
- [ ] **USER-02**: 用户可以修改密码
- [ ] **USER-03**: 系统保存用户的偏好设置（语言、阅读偏好）

---

## v2 Requirements (Deferred)

- 社交功能（评论、评分、分享）
- 移动端原生应用
- 小说推荐算法
- 批量导入导出翻译文件
- 用户生成内容（上传原创小说）
- 高级搜索和筛选

## Out of Scope

- 在线小说发布 — 专注本地源内容
- 移动端原生应用 — 优先保证 Web 体验
- 社交功能（评论、分享、点赞）— 核心是阅读和翻译

---

## Traceability

| Requirement | Phase | Status |
|------------|-------|--------|
| AUTH-01 | Phase 1 | |
| AUTH-02 | Phase 1 | |
| AUTH-03 | Phase 1 | |
| AUTH-04 | Phase 1 | |
| CONT-01 | Phase 2 | |
| CONT-02 | Phase 2 | |
| CONT-03 | Phase 2 | |
| CONT-06 | Phase 2 | |
| CONT-04 | Phase 3 | |
| CONT-05 | Phase 3 | |
| READ-01 | Phase 4 | |
| READ-02 | Phase 4 | |
| READ-03 | Phase 4 | |
| READ-04 | Phase 4 | |
| READ-05 | Phase 4 | |
| BOOK-01 | Phase 5 | |
| BOOK-02 | Phase 5 | |
| BOOK-03 | Phase 5 | |
| BOOK-04 | Phase 5 | |
| TRANS-01 | Phase 6 | |
| TRANS-02 | Phase 6 | |
| TRANS-03 | Phase 6 | |
| TRANS-04 | Phase 6 | |
| TRANS-05 | Phase 6 | |
| TRANS-06 | Phase 6 | |
| TRANS-07 | Phase 6 | |
| DEPLOY-01 | Phase 1 | |
| DEPLOY-02 | Phase 1 | |
| DEPLOY-03 | Phase 1 | |
| USER-01 | Phase 7 | |
| USER-02 | Phase 7 | |
| USER-03 | Phase 7 | |

---
*Last updated: 2026-04-27 after requirements definition*
