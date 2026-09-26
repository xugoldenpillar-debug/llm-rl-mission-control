# RL Mission Control

**30 天 · 300 小时 · 从开发工程师到可复现的后训练研究作品。**

一个中文、本地优先、零运行时依赖的 LLM Post-Training / Reasoning RL / Agentic RL 学习工作台。不是空壳模板：内置完整 **30 天、180 项任务、28 份资料入口、30 张概念卡、30 组 ML Coding / 普通算法练习、10 个知识阶段和 8 个交付里程碑**。

从零进度开始，不预填实验结果，不把任务勾选伪装成实际学习时长。课程保持 Code RL、Verifier、Credit Assignment 方向；正式大仓库和多模型规模实验留到后续，优先交付可控的小规模研究。

## 立即运行：不需要 npm install

```bash
git clone https://github.com/xugoldenpillar-debug/llm-rl-mission-control.git
cd llm-rl-mission-control
npm run dev
```

打开终端显示的 `http://127.0.0.1:8787`。Node.js 要求 22 或更高。没有 Node 也可用 Mac 自带/自行安装的 Python 3：

```bash
python3 -m http.server 8787 --bind 127.0.0.1
```

不建议双击 `index.html`：`file://` 下模块、数据库和离线能力的行为不可靠。固定使用同一个地址和端口，避免“换了来源所以看不到进度”。

首次进入：在“设置与数据”确认 Day 1、预算和学习日。每天的净学习时间是 600 分钟，休息不计入；默认每天学习，设置休息日后自动顺延30个学习日。

## 页面与功能

| 工作空间 | 已实现内容 |
| --- | --- |
| 总览 | 今日/指定学习日任务、真实进度、专注时间、欠账提示、30日热力格、近7天时长、下个里程碑 |
| 30天计划 | 全课程日历、未完成/逾期/全部任务、单项改期、欠账结转、自定义补充任务、完整计划 Markdown、ICS 日历导出 |
| 知识路线 | 明确任务依赖和阶段验收；允许提前阅读，严格模式限制越级完成；已掌握内容可记录理由豁免 |
| 资料书架 | 论文/文档/课程筛选、全局搜索、收藏、阅读状态、阅读笔记、首次使用日与具体阅读范围 |
| 复习与算法 | 概念题先回答后展开、间隔复习、30组ML Coding与普通算法链接；每日30分钟已计入10小时 |
| 实验室 | 实验CRUD、模型/数据/split/seed/config、正确数/总数、token/turns/reward/成本、原始链接、两组描述性比较、CSV |
| 研究日志 | 自动保存正文/理解/阻塞/假设/下一步；真实活动历史；每日/全部日志/周复盘导出 |
| 算力与预算 | 人民币用量×实际单价账本、预算阈值提示、费用分类、可选实例关机提醒与手动确认、CSV |
| 作品里程碑 | 8个交付物、证据链接、手动验收、作品索引导出、诚实的简历表达指导 |
| 执行手册 | Mac安装、磁盘规划、本地/云端分工、2000/3500/5000预算、隔离安全、卡住时回退、60–90天后续 |
| 设置与数据 | 日期/工作日/休息日/主题/预算/计时设置；JSON和密码加密备份；校验预览后恢复；快照；持久存储申请 |

全局：深浅色主题、响应式布局、键盘操作、离线应用壳、可安装manifest、跨标签页状态通知。按 `⌘/Ctrl K` 或 `/` 搜索，`1` 总览、`2` 计划、`?` 帮助。

## 课程与范围

| 天数 | 主线 | 每阶段需要留下什么 |
| --- | --- | --- |
| D1 | 环境与最小forward | 环境清单、logits/采样检查 |
| D2–4 | Attention / LM训练循环 / LoRA | 自主实现、数值对齐与边界测试 |
| D5–7 | SFT / DPO / Reward Model | mask审计、偏好损失与误判分析 |
| D8–11 | Policy Gradient / PPO / LLM logprob / GRPO | 公式、损失单测、零方差和token mask |
| D12–15 | Reasoning RL | 固定split和解码协议，Base/SFT/GRPO评测、reward hacking案例 |
| D16–19 | verl / rollout serving / RL系统 / DAPO | 最小环境、数据流图、吞吐/显存、一个受控变体 |
| D20–22 | 小型Code Agent / 隔离环境 / 终局RL | 可重置sandbox、60–100条小任务、严格split、outcome基线 |
| D23–25 | Verifier / Credit Assignment / 协议冻结 | 可靠测试结果解析、反例、方法边界、实验预注册 |
| D26–29 | 主实验 / 消融 / OOD / 报告 | 原始数据、seed、区间、失败分析、复现说明 |
| D30 | Release / 答辩 / 求职作品 | 可核查的证据链，不伪造提升或新算法 |

每日6个时段：理论120min、论文源码90min、实现210min、实验验收120min、ML/算法复习30min、日志交付30min。各任务包含资料、具体工作、验收、依赖和回退路线。网页“导出完整计划”可得到全量每日文档，不需要另看README猜安排。

**重要研究边界：**`R = aR_outcome + bR_tool + cR_process` 只是标量奖励塑形；只有明确实现并验证动作级回报/优势进入loss，才称逐步信用分配。VGCA-RL 是研究工作名，不代表已证明的新方法。实验为空代表未测量，而不是0分；项目没有内置训练好的模型、训练代码成果或虚构指标。学习计划不承诺录用，也不承诺30天完成算法创新。

## 数据保存：没有账号，也没有云同步

主数据在当前站点的 **IndexedDB**；localStorage 保存镜像并作为降级路径。写入通过读改写事务串行处理；多个标签页使用 BroadcastChannel 通知。每20次变更，以及导入/重置前，保留本地快照（主模式最多7份，降级模式5份）。无法持久化时明确显示“仅内存”，不会假装已安全保存。

**浏览器本地保存不能抵御清除网站数据、浏览器卸载、无痕窗口关闭、磁盘损坏或更换设备。** 快照和镜像不等于独立备份。每周通过“设置与数据”导出JSON到独立文件夹/iCloud；更换域名、端口、浏览器或设备后导入。恢复前显示任务数、学时和支出，完整替换而非不透明合并；原数据先留快照。备份导入校验schema、数值、日期、危险字段和文件大小。密码加密备份使用PBKDF2-SHA256 + AES-256-GCM，密码不保存且无法找回。

公开仓库只存应用和课程，**不会接收你的笔记、实验记录或费用**。应用无模型API调用、无遥测、无登录；点击资料链接才访问第三方。不要把API key写进日志、证据URL或Git。JSON默认未加密，私密内容建议密码加密导出。

数据语义：完成学时仅来自基础任务“已完成”；掌握豁免可满足前置，但不计完成学时。实际用时仅来自专注/手动记录；补充任务不扩大300小时基础分母。暂停后的计时不增长，运行中的计时以墙钟恢复，休息不计学习时长；离开/睡眠可能计入墙钟，可在“学习记录”校正。计时结束不自动验收任务。

## 部署

### GitHub Pages：推荐最少操作

根目录已经是可部署静态站，不需要构建即可发布：

1. 仓库 **Settings → Pages → Source → Deploy from a branch**。
2. 选择 **main / (root)**，保存。
3. 等 GitHub 的 Pages 部署完成，使用该页面显示的站点地址。

也可使用随仓库提供的构建流程：Settings → Pages → Source 选 **GitHub Actions**，然后在 Actions 手动运行 **Deploy GitHub Pages**。之后main更新会自动构建和发布。工作流先检查Pages配置；尚未启用时只完成测试/构建并提示，不假装已经部署。无需把GitHub token放进网页。

### Vercel / Netlify / Cloudflare Pages

静态构建命令 `npm run build`，产物目录 `dist`，框架选择 Other / None。已提供 `vercel.json`、`netlify.toml`；也可直接上传dist到任意HTTPS静态托管。没有数据库服务器、环境变量或运行时后端。所有资源使用相对路径，兼容GitHub Pages的仓库子路径。

```bash
npm run build
node scripts/dev.mjs --dir dist --port 8787
```

浏览器数据不会随托管迁移：迁移前导出，迁移后导入。首次在线打开会缓存应用壳；外链论文不在缓存范围内。更新时不强行替换正在运行的旧版本，备份后关闭所有工作台窗口，再重新打开。不要把私有文件放在静态服务目录。开发服务默认仅绑定127.0.0.1；对公网部署使用HTTPS静态平台。

## 测试与开发

```bash
npm test       # Node内置测试，不安装依赖
npm run check  # 语法检查 + 核心测试 + 静态构建
npm run dev    # 默认127.0.0.1:8787
```

代码结构：

```text
index.html / styles.css        页面壳、响应式和主题
js/plan.js                     课程数据、资料、阶段与里程碑
js/core.js                     纯函数、日程、进度、校验、导出、计时
js/storage.js                  IndexedDB事务、镜像、快照、跨标签页
js/views.js                    安全转义的页面视图
js/app.js                      表单、交互、导入导出、加密与事件处理
sw.js / manifest.webmanifest   版本化离线应用壳
scripts/                      本地服务和静态构建
 tests/                        自动化测试
.github/workflows/             持续测试与Pages发布
```

不在渲染函数执行网络请求；用户内容一律HTML转义，外链限制http(s)，CSV处理表格公式注入。无痕/低配额环境有降级提示。浏览器端内容加密只用于导出文件，并不声称可以抵御恶意扩展或被控制的设备。请在自己的目标浏览器上做一次备份恢复演练。

## 资料来源与核验边界

课程沿用用户确认的Post-Training / Agentic RL方向，排期与验收是本项目的教学设计；未公开用户上传原文。书架中标记“入口复核”的资料于2026-09-26查阅；其余明确标为参考入口，使用时核验版本。外部链接和软件API会变化，不宣称永远最新。

主要一手入口：[CS336](https://cs336.stanford.edu/)、[TRL SFT](https://huggingface.co/docs/trl/sft_trainer)、[TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer)、[verl Agentic RL](https://verl.readthedocs.io/en/latest/start/agentic_rl.html)、[Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)、[DeepSeekMath](https://arxiv.org/abs/2402.03300)、[DPO](https://arxiv.org/abs/2305.18290)、[DAPO](https://arxiv.org/abs/2503.14476)。TRL Agent Training API为实验性功能，务必锁定版本；verl上述页面自身更新日期为2025-07-15，不把它包装成新发布内容。

持久化依据：[MDN StorageManager.persist](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist)。浏览器可以拒绝持久化申请；仍需独立备份。部署依据：[GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。首次启用Pages是仓库设置，不等于提交代码就已经上线。

## 明确没有实现或不能保证的内容

不含账号/跨设备实时同步、真实云GPU监控/自动停机、后台系统级提醒、自动W&B/HF拉取、论文自动更新、自动判断你是否学会或研究是否显著。PWA安装入口、持久存储批准由浏览器决定。页面关闭时不能保证定时提醒。完整SWE-bench官方榜单、论文发表和求职录用不属于本应用承诺。

MIT License（应用代码和原创计划内容）；外链论文、模型、数据集保留各自许可。
