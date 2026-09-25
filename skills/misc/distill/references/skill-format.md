# 产物 skill 的格式规范

对齐本机 `skills-repo` 与 Codex 共享仓的实际约定。

## 目录结构

```
<skills-repo>/skills/<分类>/<skill-name>/
├── SKILL.md            # 必需。入口，保持瘦
├── references/         # 细节协议，按需加载
├── scripts/            # 可选，确定性操作用脚本
└── assets/             # 可选，模板类
```

分类从现有类目里挑，不要新建：`knowledge-management` / `automation` / `dev-tools` /
`documents` / `thinking` / `internet-search` / `data-science` 等。

## SKILL.md frontmatter

```yaml
---
name: <kebab-case，与目录同名>
description: "<触发词设计，见下>"
---
```

两个字段都要有。`name` 必须与目录名一致。

## description 是触发词设计，最需要打磨

它决定 skill 会不会被自动调用。写法：

- 先一句话说清这个 skill 干什么
- 再列**用户可能说的原话**作为触发词（中英文都要）
- 触发词要覆盖口语变体，不要只写书面语

反例：`description: "用于知识蒸馏。"` —— 永远不会被触发。

正例见本 skill 自己的 frontmatter。

## 渐进披露

- **SKILL.md 保持瘦**（经验值 150 行以内）：入口 + 分流表 + 硬约束 + 快速开始
- 细节放 `references/`，**按需加载，不要一次全读**
- 单文件超 300 行考虑拆分
- 大段参考资料放 `references/`，不要塞进 SKILL.md

理由：SKILL.md 每次都会进上下文，references 只在需要时加载。

## scripts/ 的边界

**脚本只做确定性操作**：格式转换、文件生成、校验。

**判断密集型环节不要写成脚本** —— 抽取、压缩、分类这类需要理解语义的，
写成给 agent 的协议（references 里的 md），由 agent 读文本后执行。

把判断塞进脚本的后果：脚本会给出看起来确定、实际没根据的结果。

## 写完之后

1. 检查 `name` 与目录名一致
2. 检查 description 里的触发词是否覆盖口语说法
3. 检查 SKILL.md 没有超长
4. **停住，等用户确认**再装进 skills-repo 并同步 Codex
