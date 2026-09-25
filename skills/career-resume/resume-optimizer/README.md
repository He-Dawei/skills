# Resume Optimizer - Claude Code Skill

基于 Claude Code 的简历优化与 HTML 生成助手。提供简历文件 + 目标岗位 JD，自动完成 JD 拆解、STAR 法重写、专业 HTML 简历输出。

## 功能特性

- **JD 智能拆解**：提取 3 个核心能力要求 + 2 个隐藏招聘偏好 + 10 个必须出现的关键词
- **STAR 法重写**：在真实经历基础上优化表达，不编造不夸大
- **证件照嵌入**：支持上传 JPG/PNG 证件照，自动缩放并 base64 内嵌，HTML 文件自包含
- **单页保障**：紧凑 CSS + JS Auto-Scale 兜底，始终输出一页 A4
- **打印就绪**：浏览器打开后 Ctrl+P 即可导出 PDF

## 目录结构

```
resume-optimizer/
├── SKILL.md                          # Skill 系统提示词
├── README.md
├── scripts/
│   └── generate_resume.py            # Python 脚本：读取简历 + 生成 HTML
└── references/
    ├── jd-analysis-rules.md          # JD 拆解方法论
    ├── star-methodology.md           # STAR 重写指南 + 示例
    └── html-resume-template.md       # HTML 模板结构文档
```

## 使用方式

### 前置条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI 或桌面端
- Python 3.8+
- Python 依赖：`PyMuPDF`、`python-docx`、`Pillow`（可选，用于证件照缩放）

### 一键安装

```bash
# 安装 Skill
git clone https://github.com/Liliane0310/resume-optimizer.git ~/.claude/skills/resume-optimizer

# 安装 Python 依赖
pip install PyMuPDF python-docx Pillow
```

> 确保本地有 Python 3.8+ 环境。

### 使用流程

在 Claude Code 中提供简历文件和 JD：

```
帮我优化简历，目标岗位是美团的内容营销实习生
简历文件：D:\简历\我的简历.pdf
JD：[粘贴 JD 文本或提供截图]
```

Claude 会自动执行以下步骤：

1. **读取简历** — 提取 PDF/Word/TXT 中的文本内容
2. **询问证件照** — 询问是否需要嵌入证件照
3. **分析 JD** — 拆解核心能力、隐藏偏好、关键词（展示给用户确认）
4. **STAR 重写** — 基于真实经历按 STAR 法重写（展示给用户确认）
5. **生成 HTML** — 输出专业商务风 HTML 简历文件

### 后续修改

生成后可随时要求定点修改：

```
项目经历第二段太笼统，换个写法
加一段关于数据分析的经历
关键词"用户增长"没有体现，加上
排版调大一点
加上证件照
```

## JSON 数据结构

```json
{
  "name": "姓名",
  "phone": "手机",
  "email": "邮箱",
  "photo": "证件照文件路径（可选，JPG/PNG）",
  "objective": "目标岗位",
  "education": {
    "school": "学校",
    "school_tag": "211/985（可选）",
    "major": "专业",
    "degree": "学历",
    "period": "时间段",
    "gpa": "GPA（可选）",
    "courses": ["课程1", "课程2"]
  },
  "experience": [
    {
      "section": "实习经历 / 校园经历 / 项目经历",
      "company": "公司/组织",
      "role": "职位",
      "period": "时间段",
      "bullets": [
        {"label": "标签名称", "text": "具体描述"}
      ]
    }
  ],
  "skills": [
    {"label": "能力类别", "text": "能力描述"}
  ]
}
```

## 脚本用法

```bash
# 读取简历文件
python scripts/generate_resume.py read <简历文件路径>

# 从 JSON 生成 HTML 简历
python scripts/generate_resume.py build <json文件> <输出路径>
```

## 设计决策

| 决策 | 方案 | 原因 |
|------|------|------|
| 依赖管理 | PyMuPDF + python-docx + Pillow | 中文提取质量好，Pillow 自动缩放证件照 |
| HTML 渲染 | Python f-string 内嵌模板 | 无 Jinja2 依赖，单模板够用 |
| JD 分析 | Claude 智能完成 | 需要语义理解，LLM 是强项 |
| 中间格式 | JSON | 脚本可独立测试，schema 清晰 |
| 照片处理 | Pillow 缩放 + base64 内嵌 | HTML 自包含，分享不丢图 |
| 单页保障 | CSS 紧凑 + JS Auto-Scale | 内容稍多也能兜底，不会溢出到第二页 |

## License

MIT
