# AI Work Hub 投资尽调 Skill

[English](README.md)

这是一个面向连续投资判断的 Codex skill。把 BP、飞书链接、datapack、访谈纪要、原文转录、财务模型或其他项目更新交给它，它会持续维护同一份项目判断，而不是每轮生成互相割裂的新结论。

## 它会做什么

- 建立统一的项目文件夹，保存原始资料、解析文本和输出文档。
- 维护一份持续更新的投资判断和核心 todo。
- 每轮问题清单、访谈提纲和重整纪要单独生成带日期的文件。
- 区分已核验信息、公司/来源自述和待核验事项。
- 在可能改变判断时，查询公开信息和核心技术团队背景。
- 在价格重要时，参考合适的美股、A 股、港股和一级市场可比。
- 可选连接本地私有的 AI Work Hub Memory Graph，调用历史项目和跨项目认知。
- 用户确认不投后归档项目，并保留重新打开的条件。

默认输出以投资决策为中心：`投`、`继续推进`、`暂缓`或`不投`，随后说明最重要的事实、风险和下一步。

## 默认工作流

```text
收到新材料
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
    归档/
```

飞书通常只是资料入口，不会因为读取链接就切换到飞书存储。读取会议纪要时，在权限允许的情况下同时读取智能纪要和原文转录；发生冲突时，以原文为准。

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
