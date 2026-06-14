# Chrome 插件 — 30 秒安装

1. 打开 Chrome，地址栏输入 **`chrome://extensions/`**
2. 右上角打开 **「开发者模式」**
3. 点击 **「加载已解压的扩展程序」**
4. 选择本仓库的 **`chrome_extension/`** 文件夹
5. 点击工具栏上的 🚀 图标即可使用

## 功能

- 弹窗：选场景 → 运行 v8 分析 → 东财条件单
- 浮标：在东方财富 / 同花顺页面右下角显示快捷入口

## 首次使用

若缺少图标，在项目根目录运行：

```bash
python3 scripts/generate_icons.py
```

或 `make chrome`

⚠️ 演示工具，不构成投资建议。
