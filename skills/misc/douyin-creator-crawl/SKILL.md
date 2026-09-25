---
name: douyin-creator-crawl
description: "批量抓取抖音博主主页的全部作品数据（文案、发布时间、点赞/评论/转发/收藏、话题、音乐、视频地址），可选下载视频文件。触发词：抓取这个博主、把这个抖音号的作品都抓下来、批量抓抖音、爬这个博主的所有视频、抖音博主数据、抖音主页批量、导出抖音作品列表、扒这个博主。用户给出抖音博主主页链接或任意一条该博主的视频链接，并要求「批量」「全部作品」「导出数据」时使用。单条视频的文案提取请用 douyin-video。"
---

# 抖音博主主页批量抓取

走浏览器实况拦截，**不碰 msToken / a_bogus** —— 让 Edge 自己算，我们只收割
`/aweme/v1/web/aweme/post/` 的 JSON 响应。这条路绕开了 yt-dlp 与 douyin-downloader
在本机长期卡住的两个死结。

## 命令

```bash
python C:/Users/44527/douyin-tools/scripts/creator_crawler.py \
    --link "<博主链接>" --output "<输出目录>" [--download] [--max-pages 30] [--headful]
```

用户桌面另有 `抖音博主批量抓取.lnk`，双击即可，供用户自己跑。

## 链接怎么给（踩过的坑）

**抖音「分享」复制出来的是整段文本，不是链接**，长这样：

```
9.99 07/02 Qkp:/ J@v.sE :3pm 今天我们来学习… #程序员 #python教学  https://v.douyin.com/oky-Go5ZAiU/ 复制此链接，打开Dou音搜索，直接观看视频！
```

整段直接粘即可 —— 脚本会自己挑出 URL。**不要试图手动裁剪**，也不要因此报错说链接无效。
实测第一次接入就是被这个卡住的（`Cannot navigate to invalid URL`）。

## 链接从哪来

必须是 **抖音 App「分享主页」复制的 `v.douyin.com/xxx/` 短链**。

- 也可以用单条视频的分享链接 —— 脚本会先解析作者，再抓其主页
- **不要用 `douyin.com/user/{抖音号}`** —— 会静默失效（页面是 SPA 空壳）
- 抖音号（unique_id）拿不到，必须用 sec_uid

## 输出

```
<输出目录>/
├── creator_<sec_uid>.jsonl        每行一条作品
├── creator_<sec_uid>.summary.json 汇总
└── videos/<日期>_<aweme_id>_<标题>.mp4   仅 --download 时
```

字段：`aweme_id` / `desc` / `create_time` / `create_time_iso` / `media_type`(`video`|`image`) /
`duration_ms` / `digg_count` / `comment_count` / `share_count` / `collect_count` /
`video_url` / `video_url_list` / `cover_url` / `music_title` / `hashtags` / `author_sec_uid` 等。

### 两个字段拿不到，别承诺

- **`play_count`（播放量）恒为 0** —— 网页端接口不返回，只有创作者自己后台能看到
- **`author_unique_id`（抖音号）为空** —— 同理

要这两个字段只能逐条开视频页，代价 20–30 秒/条。用户没明确要求就别做。

评论正文需要另调 `aweme/v1/web/comment/list/`，风控更敏感，默认不做。

**图文帖**（`media_type: "image"`）走 `images[]` 分支，`video_url_list` 里放的是图片地址。实测一个 405 条作品的博主里有 27 条图文，别假设全是视频。

## 风控：必须先说清楚的三件事

1. **同一个博主短时间内反复抓会被拦。** 两次之间隔 10 分钟以上。
   实测把 profile 打到弹滑块，只需连跑几次。
2. **滑块验证由用户本人完成，不要尝试自动过。** 脚本识别到验证页会直接报错并说明。
   处理方式：加 `--headful` 让窗口显示，用户手动滑一次；凭据留在 Edge profile 里，之后可照常无头跑。
3. **该 Edge profile 与 `ShareToObsidianSync` 任务共用。** 被标记会连带影响同步任务。
   脚本启动前会查进程表，发现 sync_service 占用会拒跑（防 Chromium exitCode 21）。

## 常见报错

| 输出 | 含义 | 处理 |
|---|---|---|
| `抖音返回验证页` | 被风控 | 加 `--headful`，让用户手动过滑块 |
| `未收到任何作品响应` | 链接无效 / 没登录 / 私密账号 | 先 `--headful` 看实际页面 |
| `链接落到视频页但…没能解析出作者` | 三级回退全失败 | 改用「分享主页」复制的短链 |
| `检测到 N 个进程正在使用 Edge profile` | 与 sync_service 抢 profile | 先停 sync_service，或 `--allow-shared-profile` |

## 抓取中断

脚本会在中断时**保存已收到的数据**再以非零退出码退出。
部分结果仍写进了 `.jsonl`，可直接用，不必从头重跑。

## 与 douyin-video 的区别

- `douyin-video` —— **单条**视频的无水印下载 + 文案（走硅基流动 API），用于处理用户发来的一条链接
- 本 skill —— **整个博主主页的批量**作品数据导出

用户说「这个博主」「全部作品」「批量」→ 本 skill。
用户发来单条视频说「提取文案」→ douyin-video。
