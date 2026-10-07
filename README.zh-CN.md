# AI Work Hub Diligence

[English](README.md)

**持续项目判断**。把 BP、datapack、访谈和项目更新接到同一份投资判断。首次给材料即可建档，后续补资料持续更新，而不是每轮另写一份结论。

## 安装与更新

也可以直接让 Codex 从此 GitHub 仓库安装 Skill，并先检查是否已有安装。推荐 Git 克隆加单个软链接，让自用版和分享版使用同一源码：

```bash
mkdir -p ~/Documents/skills-repos ~/.codex/skills
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
ln -s "$(pwd)/ai-work-hub-diligence-skill/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

已有同名目录时先检查，不覆盖安装，避免出现重复 Skill。Python 脚本需要 Python 3.10+；Graph 共享锁支持 macOS/Linux。安装后重新加载 Codex。更新时：

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull --ff-only
```

软链接立即使用同一份代码，无需复制另一份 Skill。私人工作区与仓库分开。

## 日常使用

直接发送 BP 或项目相关材料，也可明确写：

```text
用 $ai-work-hub-diligence 看这个 BP，建立项目并给初步判断和简短问题清单。
这是后续飞书交流链接，请读原文并更新同一份判断和核心 todo。
为这个项目准备下一轮客户访谈问题。
只在对话里分析，不生成文件。
```

首次使用确认私人工作区路径；首次新建项目将任务改名为 `Project 项目名`，之后不反复检查。默认目录：

```text
项目/<项目名>/
  原始资料/
  解析文本/
  输出文档/
    <项目名>_项目判断与todo.md
    <项目名>_项目状态.json
    01_问题清单/       # 按需
    02_交流纪要/       # 按需
    03_研究与分析/     # 按需
    04_正式交付/       # 按需
  工作区/              # 可重建的过程文件，按需
项目/归档/
```

判断先讲业务逻辑、最有力的反对理由与下一步：投 / 继续推进 / 暂缓 / 不投。初筛可使用有来源的公司数据，不默认索取流水、协议或做工程测试。技术团队背景、估值可比和追加核查按重要性展开。确认 pass 后再归档。

飞书是资料入口，纪要会寻找原始文字记录及相关链接，不只读智能纪要。首次配置由 agent 按 [飞书 CLI 指引](ai-work-hub-diligence/references/feishu-cli.md) 协助安装、登录、申请必要权限并测试目标文档；仓库不提供凭据。

[首次建档与改名](ai-work-hub-diligence/references/project-setup.md)保留专用工具 → 官方 App Server → 读回确认的完整流程。目录迁移和全量审计属于维护，不是每次尽调前置动作。[虚拟案例](examples/virtual-cases/README.zh-CN.md)展示初筛推进、停止跟进和多轮更新，均为脱敏虚构材料。

## 三个 Skill 如何衔接

[尽调](https://github.com/guyu980/ai-work-hub-diligence-skill)维护单公司现行判断；[Memory Graph](https://github.com/guyu980/ai-work-hub-memory-graph-skill)整理非项目来源和跨项目记忆；[深度研究](https://github.com/guyu980/ai-work-hub-deep-research-skill)负责明确要求的正式报告。安装同伴 Skill 可以联动，也可单独使用。新闻与 GitHub 发现由已授权的自动化任务执行，Skill 本身不自动创建定时任务。

公开仓库只保存通用机制、脚本和虚拟案例。实际项目、知识库、报告、私人关注名单、交付地址和凭据保留本地，不上传。贡献通过 PR，由维护者审阅合并。模型选择属于运行设置，Skill 不绑定某个模型。

[Agent 执行入口](ai-work-hub-diligence/SKILL.md) · [MIT](LICENSE)
