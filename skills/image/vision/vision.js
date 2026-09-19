#!/usr/bin/env node
/**
 * Vision skill — 调用视觉模型识图，OpenAI 兼容格式。
 * 实际模型由 .env 的 VISION_MODEL 决定（当前为 deepseek-v4-flash-vision-exp）。
 *
 * 用法:
 *   node vision.js <图片路径> [问题]
 *   node vision.js --url <图片链接> [问题]
 *
 * 配置: 同目录 .env 文件或环境变量
 *   DASHSCOPE_API_KEY — 阿里云百炼 API Key
 *   VISION_MAX_TOKENS — 单次最大输出 token（默认 4096，推理模型勿调小）
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

// 加载 .env（脚本所在目录 + 当前目录）
try { require("dotenv").config({ path: path.resolve(__dirname, ".env") }); } catch {}
try { require("dotenv").config(); } catch {}

const BASE_URL = process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com/compatible-mode/v1";
const API_KEY = process.env.DASHSCOPE_API_KEY || "";
const MODEL = process.env.VISION_MODEL || "qwen3.5-omni-plus-2026-03-15";

function parseArgs() {
  const argv = process.argv.slice(2);
  let imageSource = "", prompt = "", isUrl = false;

  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--url" && argv[i + 1]) {
      isUrl = true;
      imageSource = argv[++i];
    } else if (!imageSource && !argv[i].startsWith("--")) {
      imageSource = argv[i];
    } else if (imageSource && !argv[i].startsWith("--")) {
      prompt = prompt ? prompt + " " + argv[i] : argv[i];
    }
  }
  if (!prompt) prompt = "请详细描述这张图片的内容。";
  return { imageSource, prompt, isUrl };
}

function resolveImageUrl(source, isUrl) {
  if (isUrl) return source;
  const resolved = path.resolve(source);
  if (!fs.existsSync(resolved)) throw new Error(`File not found: ${resolved}`);
  const ext = path.extname(resolved).toLowerCase().replace(".", "");
  const mimeMap = { jpg: "jpeg", jpeg: "jpeg", png: "png", gif: "gif", webp: "webp", bmp: "bmp" };
  const data = fs.readFileSync(resolved);
  return `data:image/${mimeMap[ext] || "jpeg"};base64,${data.toString("base64")}`;
}

function request(payload) {
  const url = new URL(BASE_URL.replace(/\/?$/, "/") + "chat/completions");
  const body = JSON.stringify(payload);
  const transport = url.protocol === "https:" ? https : http;

  return new Promise((resolve, reject) => {
    const req = transport.request(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    }, (res) => {
      let data = "";
      res.on("data", (c) => data += c);
      res.on("end", () => {
        if (res.statusCode >= 400) return reject(new Error(`API ${res.statusCode}: ${data.slice(0, 300)}`));
        try {
          resolve(JSON.parse(data)?.choices?.[0]?.message?.content || data);
        } catch { resolve(data); }
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  if (!API_KEY) {
    console.error("Error: DASHSCOPE_API_KEY not set.");
    console.error("Edit ~/.claude/skills/vision/.env or set environment variable.");
    console.error("Get key: https://bailian.console.aliyun.com/");
    process.exit(1);
  }
  const { imageSource, prompt, isUrl } = parseArgs();
  if (!imageSource) {
    console.error("Usage: node vision.js <image-path> [question]");
    console.error("       node vision.js --url <image-url> [question]");
    process.exit(1);
  }
  try {
    const imageUrl = resolveImageUrl(imageSource, isUrl);
    const result = await request({
      model: MODEL,
      messages: [{ role: "user", content: [
        { type: "image_url", image_url: { url: imageUrl } },
        { type: "text", text: prompt },
      ]}],
      stream: false,
      // max_tokens 必须留足。当前 .env 配的模型是推理模型，会先输出
      // reasoning_content 再输出 content。中文约 1 token/字，实测单帧
      // reasoning 可达 2200 字。原值 1024 会被思考吃光，导致 content
      // 返回空字符串 —— 而且不报错，静默失败。实测长 prompt 下 38/43 帧中招。
      max_tokens: Number(process.env.VISION_MAX_TOKENS || 4096),
    });
    console.log(result);
  } catch (err) {
    console.error("Vision error:", err.message);
    process.exit(1);
  }
}

main();
