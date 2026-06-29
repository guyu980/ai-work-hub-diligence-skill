# AI Work Hub 尽调 Skill

[English](README.md)

这是一个用于持续项目尽调的 Codex skill，适合公司内部做早期项目初筛、资料归档、飞书纪要读取、问题清单生成和多轮判断更新。

它不是一次性 memo 模板，而是一套工作流：用户每次丢进 BP、飞书链接、datapack、交流纪要、访谈原文或其他项目材料，Codex 都会围绕同一个项目文件夹持续更新判断。

## 它能做什么

- 根据 BP、飞书链接或项目材料创建/定位项目文件夹。
- 归档原始资料、飞书抓取内容和解析文本。
- 读取飞书智能纪要，并尽量继续找到和读取原文/文字记录。
- 维护同一个项目的运行中判断与 todo 文档。
- 每轮单独生成问题清单，不覆盖历史问题清单。
- 做轻量公开信息交叉验证。
- 给出明确投资判断：`投`、`继续推进`、`暂缓`、`不投`。
- 用户确认 pass 后，将项目移动到归档文件夹。

## 推荐目录结构

首次使用时，skill 会先确认用户自己的工作区根目录，例如：

```text
~/Documents/AI Work Hub
```

项目目录建议为：

```text
<workspace_root>/
  项目/
    <项目名>/
      原始资料/
      解析文本/
      输出文档/
    归档/
```

每个 active 项目会维护一个主判断文档，例如：

```text
<workspace_root>/项目/<项目名>/输出文档/<项目名>_项目判断与todo.md
```

问题清单会每轮单独生成，例如：

```text
2026-06-29_初步问题清单.md
2026-06-29_创始人访谈问题清单.md
2026-06-29_客户访谈问题清单.md
```

## 安装说明

通过 GitHub 安装很简单：拿到 repo 权限后，clone 到本地，再把 skill 文件夹软链到 Codex 的 `~/.codex/skills/` 目录即可。后续更新只需要 `git pull`。

### 1. 申请 repo 权限

这个 repo 当前是 private。第一次安装前，先让 repo owner 把你的 GitHub 账号加入访问权限。

如果 clone 时报错 `Repository not found` 或权限不足，通常就是还没有 repo 权限，或者本机 GitHub 账号没有登录。

### 2. Clone 到本地

```bash
mkdir -p ~/Documents/skills-repos
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
cd ai-work-hub-diligence-skill
```

### 3. 软链到 Codex skills 目录

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

如果本地已经有同名 skill，先备份旧版本：

```bash
mv ~/.codex/skills/ai-work-hub-diligence ~/.codex/skills/ai-work-hub-diligence.backup
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

### 4. 验证安装

```bash
ls -la ~/.codex/skills/ai-work-hub-diligence
```

如果看到它指向刚 clone 的 repo 目录，例如：

```text
~/.codex/skills/ai-work-hub-diligence -> ~/Documents/skills-repos/ai-work-hub-diligence-skill/ai-work-hub-diligence
```

说明安装成功。

如果 Codex 没有立刻识别到这个 skill，可以新开一个 Codex 对话，或者重启/刷新 Codex。

### 5. 后续更新

进入 repo 目录后拉取最新版本：

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull
```

因为安装方式是软链，`git pull` 后 Codex 读到的就是最新版，不需要重新复制文件。

### 6. 常见问题

- `Repository not found`：确认 GitHub 账号已被加入 private repo 权限。
- `Permission denied`：确认本机 GitHub 已登录，或使用 GitHub CLI 执行 `gh auth login`。
- `File exists`：说明本地已有同名 skill，先备份或删除旧软链。
- Codex 没识别：新开对话或刷新 Codex。

## 第一次使用

看 BP 并生成初步判断：

```text
Use $ai-work-hub-diligence to review this BP, create a project folder, and give an initial judgment plus a short question list.
```

读取飞书纪要并更新判断：

```text
Use $ai-work-hub-diligence. 这是飞书纪要链接，请读取智能纪要和原文，然后更新项目判断和核心 todo。
```

准备创始人访谈问题：

```text
Use $ai-work-hub-diligence to prepare a founder interview question list for this project.
```

只想在聊天里看结果、不生成文件：

```text
Use $ai-work-hub-diligence to review this BP. 不用生成文件，直接在聊天里告诉我判断。
```

## 飞书 / Lark 配置

详见：

[`ai-work-hub-diligence/references/feishu-cli.md`](ai-work-hub-diligence/references/feishu-cli.md)

推荐每个用户在自己的工作区里安装项目本地的 `@larksuite/cli`，并完成用户身份授权。常见需要的能力包括读取文档、妙记/纪要、wiki/drive 文件，以及在用户明确要求时创建或更新飞书文档。

核心原则：

- 如果用户给的是飞书链接，默认读取源文件。
- 如果是飞书智能纪要，必须尽量继续找到原文/文字记录。
- 如果飞书文档里还有其他相关链接，继续抓取并归档。
- 长文档先保存到本地文件，再从本地文件分析，避免终端输出被截断。

## 更新这个 Skill

这个 repo 应作为唯一 source of truth。

修改后：

```bash
git status
git add ai-work-hub-diligence README.md README.zh-CN.md .gitignore
git commit -m "Update diligence skill"
git push
```

其他用户更新：

```bash
git pull
```

如果使用软链安装，`git pull` 后 Codex 读取的就是最新版。

## 不要提交这些内容

不要把以下内容提交到 repo：

- 项目原始资料、BP、datapack、纪要原文
- 飞书登录态、token、`.home`
- `.tools`、`node_modules`
- 私有交易笔记
- 用户个人本地配置
- 任何密钥、app secret 或凭据

## 维护建议

- 通用流程写进 `ai-work-hub-diligence/SKILL.md`。
- 飞书 CLI、权限、命令细节写进 `ai-work-hub-diligence/references/feishu-cli.md`。
- 用户个人偏好可以放在本地私有文件，例如 `references/local-private.md`，并保持 `.gitignore` 忽略。
- 如果后续新增模板，可以加 `references/output-templates.md`。
