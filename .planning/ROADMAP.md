# Roadmap

## Phase 1: 基础设施与用户认证

**Goal**: 建立项目基础架构，实现用户注册登录系统

**Requirements**: AUTH-01, AUTH-02, AUTH-03, AUTH-04, DEPLOY-01, DEPLOY-02, DEPLOY-03

**Success Criteria**:
1. 用户可以成功注册账号并登录
2. 登录后刷新页面仍保持登录状态
3. Docker Compose 可以一键启动所有服务
4. 环境变量配置可以切换不同 AI 模型端点

**Phase Details**:
- 搭建 Python 后端框架（FastAPI）
- 配置数据库（PostgreSQL）
- 实现 JWT 认证系统
- 创建 Vue 3 前端项目
- 配置 Docker Compose 部署
- 实现注册、登录、登出、密码重置功能

---

## Phase 2: 小说源管理（爬虫）

**Goal**: 实现爬虫系统，支持从网站增量抓取小说内容

**Requirements**: CONT-01, CONT-02, CONT-03, CONT-06

**Success Criteria**:
1. 管理员可以配置爬虫目标网站
2. 系统按定时任务增量爬取小说内容
3. 用户可以手动触发特定源的爬取
4. 爬虫数据正确存储并关联到小说元数据

**Phase Details**:
- 设计小说数据模型（小说、章节、元数据）
- 实现爬虫引擎（requests + BeautifulSoup）
- 支持反爬策略（User-Agent 轮换、请求间隔）
- 实现增量抓取逻辑（记录已抓取章节）
- 创建爬虫管理界面
- 实现定时任务调度（APScheduler）

**Depends on**: Phase 1（需要数据库和用户系统）

---

## Phase 3: 小说源管理（文件导入）

**Goal**: 实现本地文件导入功能，支持多种小说文件格式

**Requirements**: CONT-04, CONT-05

**Success Criteria**:
1. 用户可以上传 TXT、EPUB 等格式的小说文件
2. 系统正确解析文件元数据（标题、作者、章节）
3. 导入的小说可以在书架中查看和管理

**Phase Details**:
- 实现文件上传接口
- 实现 TXT 文件解析器
- 实现 EPUB 文件解析器
- 实现文件元数据提取
- 创建导入管理界面

**Depends on**: Phase 1（需要数据库）

---

## Phase 4: 阅读体验

**Goal**: 实现在线阅读功能，提供良好的阅读体验

**Requirements**: READ-01, READ-02, READ-03, READ-04, READ-05

**Success Criteria**:
1. 用户可以在线阅读小说章节
2. 阅读进度自动保存，下次打开时恢复
3. 用户可以添加和访问书签
4. 用户可以调整字体大小和夜间模式
5. 用户可以查看阅读历史记录

**Phase Details**:
- 创建阅读界面组件
- 实现章节导航
- 实现阅读进度保存和恢复
- 实现书签功能
- 实现阅读设置（字体、夜间模式）
- 实现历史记录追踪

**Depends on**: Phase 1, Phase 2 或 Phase 3（需要有小说内容）

---

## Phase 5: 书架管理

**Goal**: 实现书架和搜索功能，帮助用户管理小说

**Requirements**: BOOK-01, BOOK-02, BOOK-03, BOOK-04

**Success Criteria**:
1. 用户可以搜索小说（按标题、作者）
2. 用户可以浏览分类和标签
3. 用户可以添加/移除书架中的小说
4. 小说详情页显示完整信息（元数据、章节、翻译状态）

**Phase Details**:
- 实现搜索功能（全文搜索）
- 实现分类和标签系统
- 创建书架管理界面
- 实现小说详情页面
- 实现翻译状态展示

**Depends on**: Phase 2 或 Phase 3（需要有小说数据）

---

## Phase 6: 翻译模块

**Goal**: 实现基于大模型的翻译系统，支持多模型和可控并发

**Requirements**: TRANS-01, TRANS-02, TRANS-03, TRANS-04, TRANS-05, TRANS-06, TRANS-07

**Success Criteria**:
1. 系统可以对接多种大模型（OpenAI、Claude、本地模型）
2. 用户可以选择翻译整本书或单个章节
3. 翻译并发数可配置
4. 翻译任务队列正确管理（开始、暂停、取消）
5. 翻译结果保存到本地源
6. 用户可以实时查看翻译进度

**Phase Details**:
- 设计多模型对接架构（统一接口）
- 实现 OpenAI API 对接
- 实现 Claude API 对接
- 实现本地模型对接（Ollama/vLLM）
- 实现翻译任务队列系统
- 实现可控并发处理
- 创建翻译管理界面
- 实现翻译结果保存

**Depends on**: Phase 1（需要 API 密钥配置）

---

## Phase 7: 用户系统完善

**Goal**: 完善用户个人资料和偏好设置

**Requirements**: USER-01, USER-02, USER-03

**Success Criteria**:
1. 用户可以查看和编辑个人资料
2. 用户可以修改密码
3. 用户的偏好设置（语言、阅读偏好）被保存和应用

**Phase Details**:
- 实现个人资料编辑
- 实现密码修改功能
- 实现用户偏好设置保存
- 实现偏好设置在阅读界面的应用

**Depends on**: Phase 1（需要用户认证系统）

---

## Phase 8: 集成测试与优化

**Goal**: 全面测试所有功能，优化性能和用户体验

**Requirements**: 全量需求验证

**Success Criteria**:
1. 所有 v1 需求都已实现并通过验证
2. 系统性能满足响应时间要求
3. Docker Compose 部署流程顺畅
4. 无重大 bug 或安全问题

**Phase Details**:
- 端到端功能测试
- 性能优化
- 安全审计
- 文档完善
- 部署流程验证

**Depends on**: Phase 1-7（所有功能阶段）

---

## Coverage Validation

| Phase | Requirements | Count |
|-------|-------------|-------|
| Phase 1 | AUTH-01, AUTH-02, AUTH-03, AUTH-04, DEPLOY-01, DEPLOY-02, DEPLOY-03 | 7 |
| Phase 2 | CONT-01, CONT-02, CONT-03, CONT-06 | 4 |
| Phase 3 | CONT-04, CONT-05 | 2 |
| Phase 4 | READ-01, READ-02, READ-03, READ-04, READ-05 | 5 |
| Phase 5 | BOOK-01, BOOK-02, BOOK-03, BOOK-04 | 4 |
| Phase 6 | TRANS-01, TRANS-02, TRANS-03, TRANS-04, TRANS-05, TRANS-06, TRANS-07 | 7 |
| Phase 7 | USER-01, USER-02, USER-03 | 3 |
| Phase 8 | 全量验证 | - |
| **Total** | | **32** |

All v1 requirements mapped ✓

---
*Last updated: 2026-04-27 after roadmap creation*
