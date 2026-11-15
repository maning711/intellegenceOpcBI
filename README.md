# 世界脉搏 World Pulse

本地技术情报 Web 看板。Python 3.9+，无需第三方依赖。

## 运行

```sh
python3 server.py
```

打开 http://127.0.0.1:8765 。首次启动自动抓取，服务运行期间每 24 小时更新。页面每分钟读取缓存，也可手动刷新。停机期间不更新，重启补更。

```sh
python3 server.py --refresh # 单次抓取，可交给系统定时任务
python3 server.py --port 9000
```

## 三个标签页

- 数据库：PostgreSQL、MongoDB、AWS Database、Azure SQL 的技术及业务动态。
- AI：TechCrunch AI、Google Research、Hugging Face，自动生成候选应用、前提、验证方案、指标与风险。
- FDE：前线部署工程师，聚合 Simon Willison、The New Stack 的 Agent、集成、生产部署等关联信号，配合编辑展望框架。

分析为标题和 RSS 摘要驱动的规则初评，未接大模型，未核验正文。FDE 展望是编辑框架，不是自动新闻研究。新闻保留原语言，全球覆盖不保证完整。默认近 7 天，可搜索及调整日期范围。未提供日期的文章仅在全部时间展示。

来源失败会保留上次缓存并标记，信息源面板显示错误。可修改 server.py 中的 SOURCES。缓存 data/news.json 不入 Git，不预填模拟新闻。服务仅监听本机。

本目录为独立本地 Git 仓库，未设置远程仓库。用 git status / git log 查看版本。

## 中英文对照、周报与 OPC

- 使用提供的「且听风云」Logo。英文新闻保留标题与原文摘要，中文标题和摘要在卡片进入视口时自动翻译，逐条排队；翻译结果缓存在 data/translations.json，可点击重试。
- 翻译使用 MyMemory 公共服务，将公开新闻标题和摘要发给该服务；不需要密钥。免费额度或网络失败时显示原因并保留原文，无法保证所有文章即时译完。当前针对英文到简体中文，不是全文翻译。
- 各标签顶部生成滚动 168 小时小结，展示主题匹配数量、新闻依据、学习内容和一周实践任务。不受列表搜索或日期筛选影响。规则分析不代表行业全量趋势；无新闻时不生成结论。
- AI OPC（One Person Company，一人公司）合并 AI 与 FDE 新闻，以及 Ask HN 的 AI 相关需求讨论，提供潜在客户、最小产品、获客验证与成本核算建议。它们是待验证的创业假设，不是已确认的市场需求。

验证：`python3 -m unittest -v`，`node --check static/app.js`，`node test_frontend.cjs`。
