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
