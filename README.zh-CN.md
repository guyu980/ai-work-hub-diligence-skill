# AI Work Hub 投资尽调 Skill

[English](README.md)

这是一个面向连续投资判断的 Codex skill。把 BP、飞书链接、datapack、访谈纪要、原文转录、财务模型或其他项目更新交给它，它会持续维护同一份项目判断，而不是每轮生成互相割裂的新结论。

## 它会做什么

- 建立统一的项目文件夹，保存原始资料、解析文本和输出文档。
- 新项目初始化时一次性将任务命名为 `Project <项目名>`。
- 维护一份持续更新的投资判断和核心 todo。
- 每轮问题清单、访谈提纲和重整纪要单独生成带日期的文件。
- 区分已核验信息、公司/来源自述和待核验事项。
- 在可能改变判断时，查询公开信息和核心技术团队背景。
- 在价格重要时，参考合适的美股、A 股、港股和一级市场可比。
- 可选连接本地私有的 AI Work Hub Memory Graph，调用历史项目和跨项目认知。
- 自动识别非项目专家访谈或主题资料，并转交知识来源流程，不误建项目。
- 用户确认不投后归档项目，并保留重新打开的条件。

默认输出以投资决策为中心：`投`、`继续推进`、`暂缓`或`不投`，随后说明最重要的事实、风险和下一步。

## 分析尺度

决定性商业、技术与价格问题要深入，其他细节按需展开。初筛可使用注明来源的公司数据；只有不确定性足以改变下一步行动时，才追加必要核查。不默认索取银行流水、全套协议或安排工程测试。重要更新重新审视投资逻辑，普通更新只改受影响内容；日常校验本次项目，全工作区审计用于维护。

Skill 不绑定特定模型，模型选择放在运行配置中。

## 默认工作流

```text
收到新材料
  -> 先判断是项目材料还是非项目知识来源
  -> 首次创建项目时：识别项目名并一次性重命名任务
  -> 找到或创建项目
  -> 归档并阅读原文
  -> 与当前判断比较
  -> 按需做公开、团队、估值检查
  -> 更新同一份判断和核心 todo
  -> 将可复用增量同步到 Memory Graph
```

默认本地结构：

```text
<工作区根目录>/
  项目/
    <项目名>/
      原始资料/
      解析文本/
      输出文档/
        <项目名>_项目判断与todo.md
        <项目名>_项目状态.json
        01_问题清单/        # 按需创建
        02_交流纪要/        # 按需创建
        03_研究与分析/      # 按需创建
        04_正式交付/        # 按需创建
      工作区/               # 按需创建，存放可重建的过程文件
    归档/
```

`输出文档/` 根目录只保留持续判断和项目状态。项目更新直接合并进持续
判断，不另建“情况更新”版本；独立文件按用途归入问题清单、交流纪要、
研究与分析或正式交付。OCR 页面、PPT 制作目录、渲染缓存等放在可选的
`工作区/`，避免干扰日常阅读。

飞书通常只是资料入口，不会因为读取链接就切换到飞书存储。读取会议纪要时，在权限允许的情况下同时读取智能纪要和原文转录；发生冲突时，以原文为准。

不专属于单一公司的专家访谈、课程、播客、会议记录或主题材料不进入 `项目/`。它们由 `ai-work-hub-memory-graph` 轻量整理到 `知识来源/`；只有涉及具体项目判断时才由本 Skill 接手。

## 通过 GitHub 安装

```bash
mkdir -p ~/Documents/skills-repos ~/.codex/skills
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
ln -s "$(pwd)/ai-work-hub-diligence-skill/ai-work-hub-diligence" \
  ~/.codex/skills/ai-work-hub-diligence
```

如果目标路径已经存在，先确认它是旧副本、备份还是符号链接，再决定如何替换。采用 Git clone 加符号链接后，更新只需要：

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull --ff-only
```

如果 Codex 没有立即显示该 skill，重新加载或重启 Codex。

可选安装检查：

```bash
python3 ai-work-hub-diligence/scripts/check_install.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

初始化项目或检查整个工作区：

```bash
python3 ai-work-hub-diligence/scripts/init_project_state.py \
  --workspace-root "$HOME/Documents/AI Work Hub" \
  --project-name "示例项目" \
  --sector "AI原生应用与工作流"
python3 ai-work-hub-diligence/scripts/audit_workspace.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

迁移旧项目时先预览，再执行：

```bash
python3 ai-work-hub-diligence/scripts/migrate_project_layout.py \
  --workspace-root "$HOME/Documents/AI Work Hub" --all-projects
python3 ai-work-hub-diligence/scripts/migrate_project_layout.py \
  --workspace-root "$HOME/Documents/AI Work Hub" --all-projects --apply
```

迁移器会保留两个核心文件，按用途整理其余输出，并重写纯文本中的本地
路径和相对链接。Office 文件中的外部链接会被扫描并报告，但不会盲目改写。

如果 `项目/` 下还存放基金、系统设计等非公司对象，只把这些对象写入
`.ai-work-hub.json` 的排除列表。审计仍会要求其余每个项目具备标准目录、
唯一持续判断和唯一项目状态，排除项不能用来隐藏未迁移项目。

## 怎么使用

首次看 BP：

```text
使用 $ai-work-hub-diligence 看这个 BP，创建项目文件夹，给出初步投资判断和简短问题清单。
```

补充材料：

```text
使用 $ai-work-hub-diligence 读取这个飞书纪要链接，包括原文转录，然后更新同一份项目判断和核心 todo。
```

准备访谈：

```text
使用 $ai-work-hub-diligence 为这个项目准备一份聚焦的客户访谈问题清单。
```

只在对话中判断：

```text
使用 $ai-work-hub-diligence 判断这份材料，但不要生成文件。
```

非项目专家访谈应使用配套的 Memory Graph Skill：

```text
使用 $ai-work-hub-memory-graph 整理这份专家访谈；它不属于单一项目。保留原文，形成核心整理，并把真正可复用的认知写回图谱。
```

## 可选 Memory Graph

如果希望新项目自动联想到历史项目、反例、赛道判断、技术主题、估值锚点、重大事件和高信号人物，可以安装配套 skill：

```bash
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-memory-graph-skill.git
ln -s "$(pwd)/ai-work-hub-memory-graph-skill/ai-work-hub-memory-graph" \
  ~/.codex/skills/ai-work-hub-memory-graph
python3 ai-work-hub-memory-graph-skill/ai-work-hub-memory-graph/scripts/init_memory_graph.py \
  --workspace-root "$HOME/Documents/AI Work Hub"
```

生成的 `Memory Graph/` 是私有工作区数据，不要上传到这个公开仓库。

## 飞书设置

公开 skill 不包含任何租户凭证。首次使用时，Codex 会按照 [`feishu-cli.md`](ai-work-hub-diligence/references/feishu-cli.md) 完成 CLI 安装、用户登录、最小权限申请和目标文档读取验证。

## 仓库边界

这个公开仓库只包含通用机制、脚本、schema 和脱敏后的虚拟案例。不要提交真实 BP、访谈原文、客户名称、项目判断、飞书 token 或生成后的 Memory Graph 内容。

其他人通过 Pull Request 提交修改，由仓库维护者审核和合并。

许可证：[MIT](LICENSE)
