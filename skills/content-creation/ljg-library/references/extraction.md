# 取景框提炼 + 手绘图解

这是 ljg-library 的命门。卡好看是壳；从一本书提炼出它独创的看世界方式（取景框）、**完整流畅清晰地讲出来**、再用一张手绘图解把它演活，才是命。失手则整张卡退化成豆瓣读书卡。

> **第一要义：完整、流畅、清晰地表达思想。** 取消一切「压成一句」「钩子要短」之类的字数约束——把这副眼睛讲透、讲顺、讲明白，永远比讲短重要。

## 一、取景框提炼（六步）

1. **问题**：这本书在回答什么问题？
2. **零点**：在它之前，人们 / 各流派怎么看这个问题（旧共识）？
3. **位移（delta）**：这本书把认知挪到哪？——新取景框就在这一步的落差里。
4. **立框（{{FRAME}}）**：用一句清晰有力的话点出这套看世界的方式——「原来不是 X，其实是 Y」的换眼睛主张。认知位移、动作动词；**禁**名词定义、**禁**「本书讲了……」式摘要。**不限字数，清晰准确高于短。** 关键词用 `<span class="hl">…</span>` 染卡身强调色。
5. **铺陈（{{EXP}}）**：把这套看世界的方式**完整、流畅、清晰地讲透**——机制、边界、为什么算位移、它改变了你怎么看什么。宁可多说几句讲明白，也不要为短牺牲清楚。关键词同样 `<span class="hl">`。
6. **校验**：删掉书名作者，{{FRAME}} + {{EXP}} 能否独立成立为「一种看世界的方式」？是摘要 → 重炼；是位移 → 过。再过翻译腔五连问（主语 / 动词 / 介词 / 定语 / 朗读卡），确保 native。

> **验收尺**：凉了的脑子，瞥一眼，那副眼睛回不回得来。

### 示例 ·《非对称风险》（遍历性）

- 问题：一个期望值为正的赌局，该不该参与？
- 零点：经典决策论用期望值（集合平均）衡量——为正就该赌，默认「一群人玩的平均」=「我玩的结果」。
- 位移：时间平均 ≠ 集合平均；你只走一条时间线，不是平行宇宙的平均；有吸收壁时正期望也通向归零。
- **立框 {{FRAME}}**：`一个赌局好不好，不看「很多人各玩一次」的平均，要看「你一个人<span class="hl">玩很久</span>」的命运。`
- **铺陈 {{EXP}}**：`经典决策论用<span class="hl">集合平均</span>判断——一百个平行的你摊平，期望为正就该上。可你不活在平行宇宙的平均里，只走<span class="hl">一条时间线</span>；路上但凡有一道<span class="hl">吸收壁</span>（破产、死亡、崩塌，进去就出不来），正期望也会把你稳稳推向归零。所以真正决定命运的是时间平均，不是集合平均。`
- 校验：删书名独立成立为一种看世界方式 ✓；朗读 native ✓

## 二、手绘图解（{{SKETCH_SVG}} + {{SKETCH_TITLE}}）

block 2 把**取景框思想演成一幕戏**，让人直观吸收。使用手绘解释的风格，白底黑墨。**主角永远是继刚本人**——直接嵌入他的墨像 `assets/ljg-portrait.png`（由其头像 `…/self/identity/head.png` 抠去牛皮纸底、只留黑墨线稿而成；像素级一致、一眼是他，比手绘小人鲜明得多）。

> 主角是固定墨像 ⇒ 不画成会走动的小人，而是**让他的肖像立在场景里当「你」，用图示 + 批注把动作演出来**。一个妙处：群众画成无脸小墨人，唯独主角有张真脸——「你 vs 一群人」不点自明。

### 视觉语法（写死，照搬）—— 白底黑墨

- **白底板** `#fdfdfb`，大留白，主体占 ~50%。
- **黑墨线** `#241a12`（`--ink`），stroke 2-2.2，线条 / 图形套 `filter="url(#rough)"` 出抖动手绘感。**文字与批注绝不 roughen**，否则糊。
- **主角** = `<image href="file:///…/assets/ljg-portrait.png">` 嵌入的继刚墨像，立在左侧（他视线朝右、望进图解里），约 200×200。
- **群众** = 微型无脸墨人（`#person`：圆头 + 水滴身 + 细腿 + 白点眼），代表「很多人 / 一群人」，正好和主角的真脸成对比。
- **批注** = `Long Cang` 手写体，黑墨 `#241a12`，配小箭头（`#ar`）。3-5 条，点关键不堆字。
- 从主角拉一根小箭头指进图示，把「你」接到他那条线 / 那个动作上。

### 怎么把「取景框思想」编成一幕戏

取景框的核心张力 → 一个空间隐喻（图示）→ 继刚墨像立在其中当「你」，箭头把他接进去。

遍历性：左侧继刚墨像（你），右侧两条命运线分叉——无脸群众在高线匀速前行（+5%），从「你」拉箭头进入那条沿时间坠向深坑（吸收壁）的线。标题「同一注，两种命运」钉住。`{{SKETCH_TITLE}}` = 图名（如 `Ergodicity 遍历性`）。

> 换书换隐喻，但**复用下面 `<defs>` 的 `#rough / #ar / #person` 和主角 `<image>`**——改的是图示（线、坑、道具、群众位置）和批注，主角墨像不变。viewBox `0 0 860 400` 配 `.plate` 刚好。
>
> **主角资产** `assets/ljg-portrait.png` 已生成。若源头像更新需重做：PIL 读 head.png，`lum<120` 的暗墨像素映射为 `#241a12`、其余设透明，再裁掉透明边即可（黑墨线稿 on 透明，落白板上就是白底墨像）。

### 遍历性整图（{{SKETCH_SVG}} 参照骨架，直接改隐喻复用）

```html
<svg viewBox="0 0 860 400" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="7" result="n"/>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="3.0" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">
          <path d="M0,1 L9,5 L0,9" fill="none" stroke="#241a12" stroke-width="1.7"/>
        </marker>
        <g id="person">
          <path d="M0,0 C-7,0 -8,-12 -3,-16 L3,-16 C8,-12 7,0 0,0 Z" fill="#241a12"/>
          <circle cx="0" cy="-20" r="5.2" fill="#241a12"/>
          <circle cx="-1.6" cy="-21" r="1.1" fill="#fff"/>
          <line x1="-2" y1="0" x2="-3" y2="7" stroke="#241a12" stroke-width="2"/>
          <line x1="2" y1="0" x2="3" y2="7" stroke="#241a12" stroke-width="2"/>
        </g>
      </defs>

      <!-- 主角：继刚本人墨像（固定，像素级一致） -->
      <image href="file:///Users/lijigang/.claude/skills/ljg-library/assets/ljg-portrait.png" x="14" y="128" width="208" height="209"/>

      <!-- 图解：双命运（roughened ink） -->
      <g filter="url(#rough)" fill="none" stroke="#241a12" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M262,118 L262,344 L800,344"/>
        <path d="M262,118 L258,128 M262,118 L266,128"/>
        <path d="M800,344 L790,340 M800,344 L790,348"/>
        <!-- ensemble high line -->
        <path d="M286,228 C420,222 640,216 786,212" stroke-dasharray="2 7" stroke-width="2.3"/>
        <!-- time line into the pit -->
        <path d="M286,244 C380,278 470,304 548,322 C588,331 624,336 652,338"/>
        <ellipse cx="694" cy="340" rx="42" ry="11.5" fill="#fdfdfb"/>
        <path d="M654,336 C654,349 734,349 734,336"/>
        <path d="M662,344 L656,357 M684,347 L680,362 M710,347 L716,362 M730,343 L737,356"/>
      </g>

      <!-- 一群无脸小人在高线匀速 -->
      <use href="#person" x="372" y="225"/>
      <use href="#person" x="468" y="221"/>
      <use href="#person" x="566" y="217"/>
      <use href="#person" x="664" y="214"/>

      <!-- 从「你」指向时间线起点 -->
      <path d="M230,250 C244,250 256,248 280,246" fill="none" stroke="#241a12" stroke-width="1.7" marker-end="url(#ar)"/>

      <!-- 墨色手写批注 -->
      <g fill="#241a12">
        <text class="hand" x="500" y="34" font-size="30" text-anchor="middle">同一注，两种命运</text>
        <text class="hand" x="600" y="190" font-size="22">很多人各玩一次  +5%</text>
        <path d="M628,198 C612,206 598,210 582,210" fill="none" stroke="#241a12" stroke-width="1.7" marker-end="url(#ar)"/>
        <text class="hand" x="338" y="332" font-size="22">你一个人玩很久</text>
        <text class="hand" x="690" y="384" font-size="22">一道吸收壁 → 0</text>
        <path d="M706,368 C700,358 692,352 686,350" fill="none" stroke="#241a12" stroke-width="1.7" marker-end="url(#ar)"/>
        <text class="hand" x="246" y="116" font-size="19">财富</text>
        <text class="hand" x="806" y="338" font-size="19">时间</text>
      </g>
    </svg>
```
