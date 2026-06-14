# Web 网页版

## 本地运行

```bash
# 在项目根目录
./scripts/serve_web.sh
# 打开 http://localhost:8080/web/
```

或使用 Make：

```bash
make web
```

## 部署

将 `web/` 目录（含 `js/v7-core.js`）上传到任意静态托管即可，例如：

- GitHub Pages
- Vercel / Netlify
- 自有 Nginx

无需后端，纯静态 HTML + JS。

## 功能

- 4 个 Demo 场景切换
- 概率条可视化
- AI 决策 / 仓位 / 止损 / 结构判断
- 一键复制完整报告
