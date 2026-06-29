# AI Work Hub 尽调 Skill

[English](README.md)

这是一个用于持续项目尽调的 Codex skill，适合公司内部做早期项目初筛、资料归档、飞书纪要读取、问题清单生成和多轮判断更新。

它不是一次性 memo 模板，而是一套工作流：用户每次丢进 BP、飞书链接、datapack、交流纪要、访谈原文或其他项目材料，Codex 都会围绕同一个项目文件夹持续更新判断。

## 它能做什么

- 根据 BP、飞书链接或项目材料创建/定位项目文件夹。
- 尝试将 Codex 对话标题设为 `Project 项目名`，项目名可用英文、中文或中文简称。
- 归档原始资料、飞书抓取内容和解析文本。
- 读取飞书智能纪要，并尽量继续找到和读取原文/文字记录。
- 维护同一个项目的运行中判断与 todo 文档。
- 每轮单独生成问题清单，不覆盖历史问题清单。
- 做轻量公开信息交叉验证。
- 给出明确投资判断：`投`、`继续推进`、`暂缓`、`不投`。
- 用户确认不再推进后，将项目移动到归档文件夹。

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

通过 GitHub 安装很简单：直接 clone 这个 public repo 到本地，再把 skill 文件夹软链到 Codex 的 `~/.codex/skills/` 目录即可。后续更新只需要 `git pull`。

### 1. Clone 到本地

这个 repo 是公开的，不需要单独申请权限：

```bash
mkdir -p ~/Documents/skills-repos
cd ~/Documents/skills-repos
git clone https://github.com/guyu980/ai-work-hub-diligence-skill.git
cd ai-work-hub-diligence-skill
```

### 2. 软链到 Codex skills 目录

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

如果本地已经有同名 skill，先备份旧版本：

```bash
mv ~/.codex/skills/ai-work-hub-diligence ~/.codex/skills/ai-work-hub-diligence.backup
ln -s "$(pwd)/ai-work-hub-diligence" ~/.codex/skills/ai-work-hub-diligence
```

### 3. 验证安装

```bash
ls -la ~/.codex/skills/ai-work-hub-diligence
```

如果看到它指向刚 clone 的 repo 目录，例如：

```text
~/.codex/skills/ai-work-hub-diligence -> ~/Documents/skills-repos/ai-work-hub-diligence-skill/ai-work-hub-diligence
```

说明安装成功。

如果 Codex 没有立刻识别到这个 skill，可以新开一个 Codex 对话，或者重启/刷新 Codex。

可选：运行安装自检。

```bash
python3 ai-work-hub-diligence/scripts/check_install.py --workspace-root "$HOME/Documents/AI Work Hub"
```

如果已经配置过飞书 / Lark CLI，可以顺便验证登录态：

```bash
python3 ai-work-hub-diligence/scripts/check_install.py \
  --workspace-root "$HOME/Documents/AI Work Hub" \
  --verify-feishu-auth
```

### 4. 后续更新

进入 repo 目录后拉取最新版本：

```bash
cd ~/Documents/skills-repos/ai-work-hub-diligence-skill
git pull
```

因为安装方式是软链，`git pull` 后 Codex 读到的就是最新版，不需要重新复制文件。

### 5. 常见问题

- `Repository not found`：确认 repo 地址是否正确，或 GitHub 页面是否能打开。
- `Permission denied`：如果使用 SSH clone，确认 SSH key；如果使用 HTTPS clone，建议直接使用上面的 HTTPS 地址。
- `git: command not found`：先安装 Git。
- 目标目录已存在：进入已有目录执行 `git pull`，或换一个目录重新 clone。
- `File exists`：说明本地已有同名 skill，先备份或删除旧软链。
- Codex 没识别：新开对话或刷新 Codex。

## 第一次使用

审阅 BP 并生成初步判断：

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

用户确认不再推进后归档：

```text
Use $ai-work-hub-diligence. 我同意这个项目不再推进，请归档项目文件夹。
```

## 虚拟案例

详见：

[`examples/virtual-cases/README.zh-CN.md`](examples/virtual-cases/README.zh-CN.md)

里面有三个完全虚拟、脱敏后的案例：

- BP 初筛后具备继续推进价值。
- BP 初筛后证据不足，建议不再推进。
- BP 初筛具备推进价值，后续持续访谈和补资料，并不断更新同一个项目判断文档。

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
git add ai-work-hub-diligence examples README.md README.zh-CN.md LICENSE .gitignore
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
- 安装、分享、协作说明写在 repo 根目录的 README 里，不放进 skill 文件夹。
- 脱敏示例放在 `examples/virtual-cases/`，且必须明确标注为虚拟案例。
- 用户个人偏好可以放在本地私有文件，例如 `references/local-private.md`，并保持 `.gitignore` 忽略。
- 如果后续新增模板，可以加 `references/output-templates.md`。
- 改完 skill 后，先跑校验再 push。

## License

MIT。详见 [`LICENSE`](LICENSE)。
