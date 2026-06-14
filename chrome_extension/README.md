# Chrome 扩展安装指南

## 加载扩展

1. 打开 Chrome，访问 `chrome://extensions/`
2. 开启右上角 **开发者模式**
3. 点击 **加载已解压的扩展程序**
4. 选择本目录 `chrome_extension/`

## 功能

- **Popup 弹窗**：点击工具栏图标，选择 Demo 场景并运行 AI 决策分析
- **页面浮标**：在东方财富、同花顺等行情页右下角显示「🧠 v7 AI决策」浮标
- **记忆场景**：自动记住上次选择的 Demo 场景

## 图标

若缺少图标，在项目根目录运行：

```bash
python3 scripts/generate_icons.py
```

## 权限说明

- `storage`：保存用户上次选择的场景
- `host_permissions`：在财经网站注入辅助浮标（只读，不采集数据）

## 免责声明

本扩展为结构概率决策演示工具，不构成投资建议。
