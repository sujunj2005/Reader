# Novel Reader Website

## What This Is

一个小说阅读网站，提供本地小说源管理（爬虫抓取 + 文件导入）、在线阅读功能和基于大模型的离线翻译模块。支持多语言翻译、多格式小说文件，以及可扩展的多模型对接。

## Core Value

高效批量导入和翻译小说，让多语言小说阅读变得简单。如果其他所有功能都失败，小说管理和翻译能力必须能正常工作。

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] 小说爬虫模块，支持从指定网站增量抓取内容
- [ ] 本地文件导入功能，支持 TXT、EPUB 等多种格式
- [ ] 在线阅读界面，支持书签、历史记录
- [ ] 书架管理，分类标签和搜索
- [ ] 用户注册、登录、个性化设置
- [ ] 翻译模块，支持对接多种大模型（OpenAI、Claude、本地部署模型）
- [ ] 按需翻译，用户可选择翻译整本书或单个章节
- [ ] 可控并发翻译，可配置最大并发数
- [ ] 爬虫定时自动抓取 + 用户手动触发都支持
- [ ] Docker Compose 一键部署所有服务
- [ ] 多用户支持，未来可能公开

### Out of Scope

- 移动端原生应用 — 优先保证 Web 体验
- 社交功能（评论、分享、点赞）— 核心是阅读和翻译
- 在线小说发布 — 专注本地源内容

## Context

- 技术栈：Python 后端 + Vue 3 前端
- 部署方式：Docker Compose 容器化
- 翻译模型：支持 OpenAI、Claude API 以及本地部署模型（如 Ollama、vLLM）
- 爬虫策略：定时增量抓取 + 用户手动触发
- 文件格式：TXT、EPUB 等多种格式
- 翻译方式：用户按需选择翻译，可控并发处理

## Constraints

- **技术栈**: Python 为主，搭配 Vue 3 — 团队熟悉度
- **部署**: Docker Compose — 本地和云端都可运行
- **并发**: 翻译需支持可控并发，避免超出 API 限制
- **扩展性**: 多模型对接架构需支持未来新增模型

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python 后端 + Vue 3 前端 | Python 生态适合爬虫和 AI 对接，Vue 3 轻量灵活 | — Pending |
| Docker Compose 部署 | 简化部署流程，本地和云端一致 | — Pending |
| 按需翻译而非全自动 | 控制成本，用户自行决定翻译范围 | — Pending |
| 多模型支持架构 | 避免单一模型依赖，灵活切换 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-27 after initialization*
