---
name: ljg-library
description: "一本书 → 一框清晰的「取景框」→ 一张 2050 图书馆借书卡（PNG）。卡上有真实封面、作者头像、书目信息；取景框 block 完整、流畅、清晰地表述该书独创的「看世界的方式」，图解 block 白底黑墨、用手绘解释风格，主角是继刚本人墨像（嵌入头像抠底而成），把这套思想演成一幕戏、直观可懂。浅色光学玻璃风、卡身强调色从封面动态提取、宽高自适应。合上书记住这副眼睛，就没白读。Use when user says '取景框卡', '图书馆卡', 'library card', '书卡', '铸书卡', '一本书一句话一张卡', '/ljg-library', or provides a book name and wants it distilled into one collectible card. NOT FOR 拆书结构分析（用 ljg-book）、纯文字金句（用 ljg-card -b）、信息图（用 ljg-card -i）、视觉笔记（用 ljg-card -v）。"
user_invocable: true
version: "2.2.0"
---

# ljg-library：取景框借书卡

一本书，铸成一张 2050 图书馆借书卡。封面、作者、书目是身份；**核心是完整、流畅、清晰地讲出这本书独创的「取景框」**（它让你换一副眼睛看世界的方式），再用一张手绘图解把这套思想演活。合上书半年后，瞥一眼这张卡，整本书改变你的那副眼睛回来——这是「没白读」的物证。

> 图解 block 用手绘解释的风格、白底黑墨，**主角是继刚本人墨像**（`assets/ljg-portrait.png`，由其头像抠底而成）。完整设计历程见 `~/.claude/PAI/MEMORY/WORK/ljg-oneliner-design/ISA.md`。

## 约束

输出为视觉文件（PNG），不适用 Org-mode / Denote / ASCII-only 规范。

## 灵魂：取景框提炼 + 手绘图解

卡好不好看是壳，**能不能从一本书提炼出它独创的看世界方式、完整流畅清晰地讲出来、再用一张手绘图解演活，才是命**。这一步若失手，整张卡退化成豆瓣读书卡。

> **第一要义：完整、流畅、清晰地表达思想。** 取消一切「压成一句」之类的字数约束——把这副眼睛讲透比讲短重要。

执行前，**先 Read `references/extraction.md`**：第一部分走六步（问题 → 零点 → 位移 → 立框 → 铺陈 → 校验）产出取景框（主句 `{{FRAME}}` + 铺陈 `{{EXP}}`）；第二部分据此把取景框思想编成一幕戏——**主角是嵌入的继刚墨像**（`assets/ljg-portrait.png`，立在场景里当「你」），右侧用图示 + 无脸群众 + 批注把动作演出来（`{{SKETCH_SVG}}`，复用其中 `<defs>` 组件与整图骨架）。

**输入弹性**：继刚常常自己已经想透（读完顺手就想铸卡）。给了思想就直接用（只走第 6 步校验 + 编图）；没给则走全程提炼。

## 视觉规格

生成 HTML 前，**先 Read `references/visual.md`**——浅色玻璃卡身规格、卡身动态色 vs 图解板白底黑墨两套配色、字体、图解板（继刚墨像主角）规格、踩过的坑全在里面。这是视觉质量底线。

## 流程

```
输入：书名（或 书名 + 已想透的取景框思想）
  ↓
1. weread 取真封面 + 书目（见下「素材获取」）
2. web 抓作者头像
3. 提封面主色 → 卡身动态强调色（python assets/extract_color.py <封面>）
4. 提炼取景框：主句 {{FRAME}} + 铺陈 {{EXP}}（完整流畅清晰；用户给了→校验，没给→走 extraction.md 六步）
5. 编手绘图解 SVG {{SKETCH_SVG}}：嵌主角墨像 assets/ljg-portrait.png + 图示 + 无脸群众 + 批注（复用 extraction.md 的 defs + 骨架，换隐喻不换主角）
6. 填 assets/library_template.html 的占位变量
7. 渲染（capture.js，fullpage 自适应高度）
8. Read 自验（含放大看图解板）→ 交付路径
```

## 素材获取（关键，按此顺序降级）

### 封面 + 书目（weread）

继刚有微信读书。走 weread skill 的 `/store/search`（先 Read `~/.claude/skills/weread/search.md`）：

```bash
curl -s -X POST "https://i.weread.qq.com/api/agent/gateway" \
  -H "Authorization: Bearer $WEREAD_API_KEY" -H "Content-Type: application/json" \
  -d '{"api_name":"/store/search","keyword":"<书名>","scope":10,"skill_version":"1.0.3"}'
```

- 回包 `results[].books[].bookInfo`（每个 result 组一本）有 `title / author / translator / cover / publisher`。
- **封面 cover URL 是 `s_` 缩略图（70×100，太小会糊）。把 `s_` 换成 `t7_` 拿高清（285×411）**：`.../cover/942/635942/t7_635942.jpg`。下载时带 `-H "Referer: https://weread.qq.com/"`。
- 取不到 weread → 联网搜豆瓣封面（web-access / markdown-proxy）→ 仍无则 CSS 占位书封。

### 作者头像（web）

维基百科原图最稳。Wikipedia API 直接拿 original 图 URL：

```bash
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  "https://en.wikipedia.org/w/api.php?action=query&titles=<英文名>&prop=pageimages&piprop=original&format=json"
# 拿到 .original.source 后下载（带 UA）：
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" -o /tmp/lib_avatar.jpg "<original-url>"
```

- **坑：thumb 路径（`/thumb/.../480px-xxx.jpg`）若该尺寸未缓存会返 HTML 错误页。用原图路径（去掉 /thumb/ 和尺寸段），并必须带 User-Agent（缺 UA 被 Wikimedia 拦）。**
- 无头像 → 省略头像（模板作者行不显示 avatar），不阻塞。

### 主角墨像（已就位）

图解板主角是继刚本人，资产 `assets/ljg-portrait.png`（黑墨线稿 on 透明，落白板上即白底墨像）已生成、固定复用，无需每次重做。源头像若更新需重做：PIL 读 head.png，`lum<120` 暗墨像素映射为 `#241a12`、其余透明，裁掉透明边。

### 卡身动态强调色

```bash
python3 assets/extract_color.py /tmp/lib_cover.jpg
# 输出形如：#c43d30
```

从封面提取最显著的**彩色**作卡身强调色（换书自动换色：红封→红卡、蓝封→蓝卡）。脚本默认挑「最频繁的彩色」——若封面主体是大面积米 / 灰背景，它会挑出发闷的背景色；**这时改按「鲜艳度 × 频次」重排，从真实像素里挑一个撑得住的彩色**（别凭空写死）。注意：这只是卡身色；图解板固定白底 `#fdfdfb` + 墨 `#241a12`，不动。

## 模板变量（library_template.html）

| 变量 | 内容 |
|------|------|
| `{{ACCENT}}` | 卡身动态强调色 hex（如 `#c43d30`，从封面提取） |
| `{{COVER}}` | 封面的 `file://` 绝对路径 |
| `{{AVATAR_IMG}}` | 整个头像 `<img class="avatar" src="file://…">`（无头像填空字符串，作者行自动省 avatar） |
| `{{TITLE}}` `{{EN}}` `{{SUBTITLE}}` | 书名中 / 英 / 副标题 |
| `{{TAGS}}` | 3-4 个主题标签（书的核心概念），每个 `<span class="tag">…</span>` |
| `{{AUTHOR_CN}}` `{{AUTHOR_META}}` | 作者中文名 / 「英文名 · 出版社 年份」 |
| `{{FRAME}}` | 取景框**主句**：清晰点出换眼睛的主张，关键词用 `<span class="hl">…</span>` 染卡身强调色 |
| `{{EXP}}` | 取景框**铺陈**：完整、流畅、清晰地把这副眼睛讲透，关键词同样 `<span class="hl">` |
| `{{SKETCH_TITLE}}` | 图解板的名字（英文 + 中文，如 `Ergodicity 遍历性`） |
| `{{SKETCH_SVG}}` | 手绘图解整段 `<svg>…</svg>`（白底黑墨、主角是嵌入的继刚墨像，见 extraction.md 第二部分） |

## 渲染

```bash
node ~/.claude/skills/ljg-card/assets/capture.js \
  /tmp/ljg_library_{name}.html ~/Downloads/{name}.png 1080 1440 fullpage
```

复用 ljg-card 的 capture.js（playwright 已装在 ljg-card/node_modules）。**必须 `fullpage`**——卡片高度自适应内容，不留底部空白。`file://` 引用本地封面 / 头像 / 主角墨像可直接渲染。

## 交付

1. Read 输出的 PNG 亲眼验图，并**放大看图解板**（封面/头像加载 ✓、取景框完整流畅讲透 ✓、卡身色协调 ✓、继刚墨像清晰是主角、群众无脸成对比 ✓、板内墨线手绘抖+批注清晰 ✓、右侧无空白 ✓）。
2. 报告文件路径 + 一句取景框提炼说明。

## Gotchas（务必避开）

- **封面尺寸**：weread `s_` 前缀是 70×100 缩略图，必糊。换 `t7_` 拿 285×411 高清，下载带 `Referer`。
- **头像 thumb 陷阱**：Wikimedia `/thumb/.../NNNpx-` 特定尺寸未缓存会返 HTML 错误页。用原图路径 + User-Agent。
- **主角是嵌入的继刚墨像，不手绘**：用 `<image href="…/assets/ljg-portrait.png">`，保证鲜明 + 像素级一致；手绘小人既不像他又每次漂移，已弃。
- **图解板是手写 SVG**：线条 / 图形套 `filter="url(#rough)"` 出手绘抖动；**文字 / 批注 / 主角墨像绝不套滤镜**（糊）。复用组件 + 骨架见 extraction.md。
- **无脸群众对真脸主角**：群众用 `#person` 无脸小墨人，唯独主角有真脸——「你 vs 一群人」靠这个对比，别给群众画脸。
- **图解板白底黑墨两色**：白 `#fdfdfb` 底 + 墨 `#241a12`。两套色别串：卡身动态色从封面提取、不写死；图解板白底 + 墨、写死。
- **取景框是认知位移不是摘要**：主句「原来不是 X，其实是 Y」+ 铺陈完整流畅讲透机制，不是「本书讲了……」。验收尺：凉脑子瞥一眼，那副眼睛回不回得来。
