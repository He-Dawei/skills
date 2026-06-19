# HTML 简历模板

本文档描述 `generate_resume.py` 实际使用的 HTML 简历模板结构。供理解和调试模板时参考。

---

## 页面布局

```
┌──────────────────────────────────────┬────────┐
│  青草蛋糕                              │        │
│  电话：111-1111-1111                 │  证件照 │
│  邮箱：xxx@qq.com                     │  108×  │
│  求职意向：内容营销实习生               │  144px │
├──────────────────────────────────────┴────────┤
│  教育背景                                      │
│  羊村大学 [211] 网络与新媒体 | 本科    2023~2027 │
│  ● 主修课程：xxx、xxx、xxx                       │
├───────────────────────────────────────────────┤
│  实习经历                                      │
│  公司名 · 职位              2025.11 ~ 2026.02  │
│  · 标签：描述内容...                            │
│  · 标签：描述内容...                            │
├───────────────────────────────────────────────┤
│  校园经历 / 项目经历（同上结构）                 │
├───────────────────────────────────────────────┤
│  岗位技能                                      │
│  · 能力标签：能力描述...                        │
└───────────────────────────────────────────────┘
```

**Header 布局**：`display: flex; justify-content: space-between`
- 左侧 `header-left`：姓名 `<h1>` + 联系方式 `.header-contact`（竖排）
- 右侧（如有照片）：`<img class="header-photo">`（108×144px）
- 无照片时：左侧占满，header 高度更紧凑

---

## CSS 设计规范

### 全局参数

| 参数 | 值 |
|------|----|
| 字体栈 | PingFang SC, Microsoft YaHei, Source Han Sans SC, sans-serif |
| 正文字号 | 13px |
| 全局行高 | 1.55 |
| 主色 | #1a1a1a（标题、姓名） |
| 正文色 | #333 |
| 辅助色 | #555 / #888（公司名、日期） |
| 分隔线 | 1px solid #ddd |
| Header 下边线 | 1.5px solid #2c3e50 |

### 页面容器

```css
.resume {
  max-width: 210mm;
  margin: 20px auto;
  padding: 18mm 20mm 14mm;   /* 上 左右 下 */
  background: white;
  box-shadow: 0 1px 6px rgba(0,0,0,0.08);
}
```

### 证件照

```css
.header-photo {
  width: 108px;
  height: 144px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
  flex-shrink: 0;
}
```

- 照片由 Python Pillow 自动缩放（max_height=288px 保证清晰度），转为 base64 内嵌
- 支持 JPG / PNG，HTML 文件自包含，不依赖外部图片

### 间距系统

| 元素 | 间距 |
|------|------|
| .section margin-bottom | 10px |
| .section-title margin-bottom | 6px |
| .section-title padding-bottom | 3px |
| .header margin-bottom | 12px |
| .header padding-bottom | 8px |
| .exp-header margin-bottom | 4px |
| .bullet-list li margin-bottom | 1px |
| .skill-item margin-bottom | 1px |
| .edu-row margin-bottom | 1px |

### 打印适配

```css
@page { size: A4; margin: 0; }
@media print {
  body { background: white; }
  .resume { margin: 0; padding: 18mm 20mm 14mm; box-shadow: none; max-width: none; }
  .section { page-break-inside: avoid; }
}
```

### 单页兜底 JS

```javascript
// 页面加载后检测内容高度，超出 A4 则等比缩放
(function() {
  var el = document.getElementById("resume");
  if (!el) return;
  var pageH = 297 - 18 - 14;  // A4高度mm - 上边距 - 下边距
  if (el.scrollHeight > pageH * 3.78) {  // 3.78 px/mm
    el.style.transformOrigin = "top left";
    var scale = (pageH * 3.78) / el.scrollHeight;
    el.style.transform = "scale(" + scale.toFixed(4) + ")";
    el.style.width = (100 / scale).toFixed(2) + "%";
  }
})();
```

---

## JSON 数据结构

`generate_resume.py build` 命令接受以下 JSON：

```json
{
  "name": "姓名",
  "phone": "手机",
  "email": "邮箱",
  "photo": "证件照绝对路径（可选，JPG/PNG）",
  "objective": "目标岗位",
  "education": {
    "school": "学校名称",
    "school_tag": "211/985/双一流（可选，不填不显示标签）",
    "major": "专业",
    "degree": "本科/硕士/博士",
    "period": "2023.09 ~ 2027.06",
    "gpa": "3.75/5.0（可选，不填不显示）",
    "courses": ["课程1", "课程2"]
  },
  "experience": [
    {
      "section": "实习经历 | 校园经历 | 项目经历",
      "company": "公司/组织名称",
      "role": "职位名称",
      "period": "2025.11 ~ 2026.02",
      "bullets": [
        {"label": "标签名称", "text": "具体描述内容"}
      ]
    }
  ],
  "skills": [
    {"label": "能力类别", "text": "能力描述"}
  ],
  "self_evaluation": "自我评价（可选，不超过3行，60-100字）"
}
```

### 字段约束

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 显示在 header 左侧大号加粗 |
| `phone` | 是 | 显示在名字下方 |
| `email` | 是 | 显示在名字下方 |
| `photo` | 否 | 绝对路径，空字符串或不填 = 无照片 |
| `objective` | 是 | 求职意向，显示在联系方式最后一行 |
| `education` | 是 | 单个对象，当前只支持一条教育记录 |
| `education.school_tag` | 否 | "211"/"985"/"双一流" 等，显示为蓝色小标签 |
| `experience` | 是 | 数组，最多 3 项 |
| `experience[].section` | 是 | 决定分组：实习经历 / 校园经历 / 项目经历 |
| `experience[].bullets` | 是 | 数组，每项 `{label, text}`，label 显示为加粗前缀 |
| `skills` | 是 | 数组，每项 `{label, text}` |
| `self_evaluation` | 否 | 纯文本字符串，不填则不显示该模块 |

### section 分组规则

`_build_experience_html` 按 `section` 字段分组：
- 相同 `section` 值的经历归入同一模块
- 模块顺序按首次出现顺序排列
- 每个模块有独立的 `<div class="section-title">` 标题

---

## generate_resume.py CLI

### 读取简历

```bash
python generate_resume.py read <file_path>
```

支持格式：`.pdf`（PyMuPDF）、`.docx`（python-docx）、`.txt`/`.md`（多编码回退）

输出 JSON：
```json
{
  "status": "success",
  "file_path": "...",
  "file_type": ".pdf",
  "text": "提取的纯文本...",
  "char_count": 1234
}
```

### 生成 HTML

```bash
python generate_resume.py build <json_file> <output_path>
```

输出 JSON：
```json
{
  "status": "success",
  "output_path": "绝对路径",
  "file_size": 12345
}
```

---

## 依赖

| 包 | 用途 | 备注 |
|----|------|------|
| PyMuPDF (`fitz`) | PDF 文本提取 | 必需 |
| python-docx | Word 文本提取 | 必需 |
| Pillow (`PIL`) | 证件照缩放 | 可选，无则原图内嵌 |
