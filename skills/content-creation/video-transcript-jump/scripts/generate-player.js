#!/usr/bin/env node
/**
 * Video Transcript Jump — 可点击时间轴跳转的视频播放器生成器
 *
 * 用法:
 *   node generate-player.js <视频路径> <字幕路径> [输出路径]
 *   node generate-player.js <视频路径> <字幕路径> --title "视频标题"
 *
 * 支持字幕格式: SRT, VTT, 纯文本 (HH:MM:SS 或 MM:SS 文本)
 */

const fs = require("fs");
const path = require("path");

// ── 解析 SRT ──
function parseSRT(text) {
  const blocks = text.trim().replace(/\r\n/g, "\n").split(/\n\n+/);
  const cues = [];
  for (const block of blocks) {
    const lines = block.trim().split("\n");
    if (lines.length < 2) continue;
    // skip index line if first line is a number
    let timeIdx = 0;
    if (/^\d+$/.test(lines[0].trim())) timeIdx = 1;
    const timeMatch = lines[timeIdx].match(
      /(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})/
    );
    if (!timeMatch) continue;
    const start =
      parseInt(timeMatch[1]) * 3600 +
      parseInt(timeMatch[2]) * 60 +
      parseInt(timeMatch[3]) +
      parseInt(timeMatch[4]) / 1000;
    const end =
      parseInt(timeMatch[5]) * 3600 +
      parseInt(timeMatch[6]) * 60 +
      parseInt(timeMatch[7]) +
      parseInt(timeMatch[8]) / 1000;
    const text = lines.slice(timeIdx + 1).join("\n").trim();
    if (text) cues.push({ start, end, text });
  }
  return cues;
}

// ── 解析 VTT ──
function parseVTT(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const cues = [];
  let i = 0;
  // skip header
  while (i < lines.length && !lines[i].includes("-->")) i++;
  while (i < lines.length) {
    const timeMatch = lines[i].match(
      /(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[.,](\d{3})/
    );
    if (timeMatch) {
      const start =
        parseInt(timeMatch[1]) * 3600 +
        parseInt(timeMatch[2]) * 60 +
        parseInt(timeMatch[3]) +
        parseInt(timeMatch[4]) / 1000;
      const end =
        parseInt(timeMatch[5]) * 3600 +
        parseInt(timeMatch[6]) * 60 +
        parseInt(timeMatch[7]) +
        parseInt(timeMatch[8]) / 1000;
      let text = "";
      i++;
      while (i < lines.length && lines[i].trim() !== "" && !lines[i].includes("-->")) {
        text += (text ? "\n" : "") + lines[i].trim();
        i++;
      }
      if (text) cues.push({ start, end, text: text.replace(/<[^>]+>/g, "") });
    } else {
      i++;
    }
  }
  return cues;
}

// ── 解析纯文本时间戳 (HH:MM:SS text 或 MM:SS text) ──
function parsePlainText(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const cues = [];
  for (const line of lines) {
    const match = line.match(
      /^(\d{1,2}):(\d{2})(?::(\d{2}))?\s+(.+)$/
    );
    if (match) {
      const h = match[3] ? parseInt(match[1]) : 0;
      const m = match[3] ? parseInt(match[2]) : parseInt(match[1]);
      const s = match[3] ? parseInt(match[3]) : parseInt(match[2]);
      const start = h * 3600 + m * 60 + s;
      cues.push({ start, end: start + 5, text: match[4] });
    }
  }
  return cues;
}

// ── 自动检测格式 ──
function parseSubtitles(text) {
  if (/\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}/.test(text)) {
    if (/^\d+\s*$/m.test(text.split("\n")[0]?.trim())) return parseSRT(text);
    return parseVTT(text);
  }
  if (/^\d{1,2}:\d{2}(?::\d{2})?\s+.+$/m.test(text)) return parsePlainText(text);
  throw new Error("Unrecognized subtitle format");
}

// ── 格式化时间 ──
function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${m}:${String(s).padStart(2, "0")}`;
}

// ── HTML 模板 ──
function buildHTML(videoPath, cues, title) {
  const cuesJSON = JSON.stringify(cues);
  const safeTitle = title || path.basename(videoPath);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${safeTitle} — 可跳转字幕播放器</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0f0f0f;color:#eee;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{padding:12px 20px;background:#1a1a1a;border-bottom:1px solid #333;display:flex;align-items:center;gap:12px;flex-shrink:0}
header h1{font-size:16px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
header .count{font-size:13px;color:#888;white-space:nowrap}
header .search{flex:1;max-width:280px}
header .search input{width:100%;padding:6px 12px;background:#252525;border:1px solid #444;border-radius:6px;color:#eee;font-size:13px}
header .search input:focus{outline:none;border-color:#5af}
main{display:flex;flex:1;overflow:hidden}
.video-panel{flex:1;display:flex;align-items:center;justify-content:center;background:#000;min-width:0}
.video-panel video{max-width:100%;max-height:100%;outline:none}
.transcript-panel{width:380px;flex-shrink:0;overflow-y:auto;background:#1a1a1a;border-left:1px solid #333;padding:0}
.transcript-panel::-webkit-scrollbar{width:6px}
.transcript-panel::-webkit-scrollbar-thumb{background:#444;border-radius:3px}
.cue{padding:10px 16px;cursor:pointer;border-bottom:1px solid #252525;display:flex;gap:10px;transition:background .15s;align-items:flex-start}
.cue:hover{background:#2a2a2a}
.cue.active{background:#1a3a4a;border-left:3px solid #5af;padding-left:13px}
.cue .time{font-size:12px;color:#888;font-variant-numeric:tabular-nums;white-space:nowrap;min-width:48px;padding-top:1px}
.cue .text{font-size:14px;line-height:1.5;color:#ddd}
.empty-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#666;gap:16px}
.empty-state svg{opacity:.4}
.shortcuts{font-size:12px;color:#555;text-align:center;line-height:1.8}
.kbd{display:inline-block;padding:1px 6px;background:#333;border-radius:3px;font-size:11px;margin:0 2px}
/* Drag overlay */
.drop-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:999;align-items:center;justify-content:center;border:3px dashed #5af;margin:20px;border-radius:16px}
.drop-overlay.show{display:flex}
.drop-overlay p{font-size:24px;color:#5af}
@media(max-width:768px){
  main{flex-direction:column}
  .video-panel{max-height:50vh}
  .transcript-panel{width:100%;flex:1}
}
</style>
</head>
<body>

<header>
  <h1>${safeTitle}</h1>
  <span class="count" id="count"></span>
  <span class="search">
    <input type="text" id="search" placeholder="搜索字幕...">
  </span>
  <span class="shortcuts">
    <span class="kbd">←</span><span class="kbd">→</span> 跳转
    <span class="kbd">Space</span> 暂停
    <span class="kbd">F</span> 搜索
  </span>
</header>

<main>
  <div class="video-panel">
    <video id="video" controls crossorigin="anonymous" src="${videoPath}"></video>
  </div>
  <div class="transcript-panel" id="transcript"></div>
</main>

<div class="drop-overlay" id="dropOverlay"><p>📁 拖放视频或字幕文件到此处</p></div>

<script>
const cues = ${cuesJSON};
const video = document.getElementById('video');
const transcript = document.getElementById('transcript');
const countEl = document.getElementById('count');
const searchEl = document.getElementById('search');
const dropOverlay = document.getElementById('dropOverlay');

// ── 渲染字幕列表 ──
let filteredCues = [...cues];
let activeIdx = -1;

function render(list) {
  if (!list.length) {
    transcript.innerHTML = '<div class="empty-state"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="7" y1="8" x2="17" y2="8"/><line x1="7" y1="12" x2="14" y2="12"/><line x1="7" y1="16" x2="10" y2="16"/></svg><p>暂无匹配字幕</p></div>';
    return;
  }
  transcript.innerHTML = list.map((c, i) => {
    const realIdx = cues.indexOf(c);
    const classes = ['cue'];
    if (realIdx === activeIdx) classes.push('active');
    return '<div class="' + classes.join(' ') + '" data-idx="' + realIdx + '">' +
      '<span class="time">' + fmt(c.start) + '</span>' +
      '<span class="text">' + esc(c.text) + '</span>' +
    '</div>';
  }).join('');

  // 绑定点击
  transcript.querySelectorAll('.cue').forEach(el => {
    el.addEventListener('click', () => {
      const idx = parseInt(el.dataset.idx);
      if (cues[idx]) {
        video.currentTime = cues[idx].start;
        video.play();
      }
    });
  });
}

function fmt(s) { const m=Math.floor(s/60); const sec=Math.floor(s%60); return m+':'+String(sec).padStart(2,'0') }
function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') }

// ── 搜索 ──
searchEl.addEventListener('input', () => {
  const q = searchEl.value.toLowerCase();
  filteredCues = q ? cues.filter(c => c.text.toLowerCase().includes(q)) : [...cues];
  render(filteredCues);
  countEl.textContent = filteredCues.length + ' / ' + cues.length + ' 条';
});

// ── 高亮当前字幕 ──
video.addEventListener('timeupdate', () => {
  const t = video.currentTime;
  let found = -1;
  for (let i = 0; i < cues.length; i++) {
    if (t >= cues[i].start && t < cues[i].end) { found = i; break; }
  }
  if (found !== activeIdx) {
    activeIdx = found;
    // 仅更新样式
    const all = transcript.querySelectorAll('.cue');
    all.forEach(el => {
      const idx = parseInt(el.dataset.idx);
      el.classList.toggle('active', idx === found);
      if (idx === found) el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  }
});

// ── 键盘快捷键 ──
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT') return;
  switch(e.key) {
    case 'ArrowRight':
      e.preventDefault();
      if (activeIdx < cues.length - 1) { activeIdx++; video.currentTime = cues[activeIdx].start; video.play(); }
      break;
    case 'ArrowLeft':
      e.preventDefault();
      if (activeIdx > 0) { activeIdx--; video.currentTime = cues[activeIdx].start; video.play(); }
      break;
    case ' ':
      e.preventDefault();
      if (video.paused) video.play(); else video.pause();
      break;
    case 'f': case 'F':
      e.preventDefault();
      searchEl.focus();
      break;
    case 'Escape':
      searchEl.value = ''; searchEl.dispatchEvent(new Event('input'));
      break;
  }
});

// ── 拖放视频/字幕 ──
let dragCounter = 0;
document.addEventListener('dragenter', e => { e.preventDefault(); dragCounter++; if(dragCounter===1) dropOverlay.classList.add('show') });
document.addEventListener('dragleave', e => { e.preventDefault(); dragCounter--; if(dragCounter===0) dropOverlay.classList.remove('show') });
document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => {
  e.preventDefault(); dragCounter = 0; dropOverlay.classList.remove('show');
  const files = e.dataTransfer.files;
  for (const f of files) {
    if (f.type.startsWith('video/')) {
      video.src = URL.createObjectURL(f);
    } else if (f.name.endsWith('.srt') || f.name.endsWith('.vtt') || f.name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        // re-parse on client using the same parsing logic (simplified)
        const newCues = window.parseClient(text);
        cues.length = 0; cues.push(...newCues);
        filteredCues = [...cues];
        activeIdx = -1;
        render(filteredCues);
        countEl.textContent = cues.length + ' 条';
      };
      reader.readAsText(f);
    }
  }
});

// ── 客户端 SRT/VTT 解析 (简化,用于拖放) ──
window.parseClient = function(text) {
  text = text.replace(/\\r\\n/g, '\\n');
  // try SRT
  if (/^\\d+\\s*$/m.test(text.split('\\n')[0]?.trim())) {
    const blocks = text.trim().split(/\\n\\n+/);
    const out = [];
    for (const b of blocks) {
      const ls = b.trim().split('\\n');
      let ti = 0;
      if (/^\\d+$/.test(ls[0]?.trim())) ti = 1;
      const m = ls[ti]?.match(/(\\d{2}):(\\d{2}):(\\d{2})[,.](\\d{3})\\s*-->\\s*(\\d{2}):(\\d{2}):(\\d{2})[,.](\\d{3})/);
      if (!m) continue;
      out.push({
        start: +m[1]*3600+ +m[2]*60+ +m[3]+ +m[4]/1000,
        end: +m[5]*3600+ +m[6]*60+ +m[7]+ +m[8]/1000,
        text: ls.slice(ti+1).join('\\n').trim()
      });
    }
    return out;
  }
  // try VTT
  if (/-->/.test(text)) {
    const ls = text.split('\\n');
    let i = 0;
    while (i < ls.length && !ls[i].includes('-->')) i++;
    const out = [];
    while (i < ls.length) {
      const m = ls[i]?.match(/(\\d{2}):(\\d{2}):(\\d{2})[.,](\\d{3})\\s*-->\\s*(\\d{2}):(\\d{2}):(\\d{2})[.,](\\d{3})/);
      if (m) {
        let txt = ''; i++;
        while (i < ls.length && ls[i].trim() && !ls[i].includes('-->')) { txt += (txt?'\\n':'') + ls[i].trim(); i++; }
        out.push({start:+m[1]*3600+ +m[2]*60+ +m[3]+ +m[4]/1000, end:+m[5]*3600+ +m[6]*60+ +m[7]+ +m[8]/1000, text:txt.replace(/<[^>]+>/g,'')});
      } else i++;
    }
    return out;
  }
  return [];
};

// ── 初始化 ──
render(filteredCues);
countEl.textContent = cues.length + ' 条';
</script>
</body>
</html>`;
}

// ── main ──
async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("用法: node generate-player.js <视频路径> <字幕路径> [输出路径] [--title 标题]");
    process.exit(1);
  }

  const videoPath = path.resolve(args[0]);
  const subPath = path.resolve(args[1]);

  if (!fs.existsSync(subPath)) throw new Error(`字幕不存在: ${subPath}`);
  if (!fs.existsSync(videoPath)) {
    console.warn(`⚠️  视频文件不存在: ${videoPath}`);
    console.warn("   HTML 已生成，但需要有效视频路径或 URL 才能播放。");
  }

  let title = path.basename(videoPath, path.extname(videoPath));
  let outputPath = path.resolve(
    path.dirname(videoPath),
    path.basename(videoPath, path.extname(videoPath)) + "-transcript.html"
  );

  // parse extra args
  for (let i = 2; i < args.length; i++) {
    if (args[i] === "--title" && args[i + 1]) title = args[++i];
    else if (!args[i].startsWith("--")) outputPath = path.resolve(args[i]);
  }

  const subText = fs.readFileSync(subPath, "utf-8");
  const cues = parseSubtitles(subText);

  if (!cues.length) throw new Error("未能从字幕文件中解析出任何时间轴条目");

  const html = buildHTML(videoPath, cues, title);
  fs.writeFileSync(outputPath, html, "utf-8");

  console.log(`✅ 播放器已生成: ${outputPath}`);
  console.log(`   ${cues.length} 条字幕, 点击时间轴即可跳转`);
  console.log(`   用浏览器打开即可使用`);
}

main().catch(err => {
  console.error("❌", err.message);
  process.exit(1);
});
