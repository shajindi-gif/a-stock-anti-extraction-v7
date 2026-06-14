# 微信小程序

## 导入项目

1. 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 选择 **导入项目**
3. 目录选择本仓库的 `miniprogram/` 文件夹
4. AppID 可选择 **测试号** 或使用 `touristappid`（仅本地预览）

## 功能

- v8 执行闭环（订单路由 / 重平衡）
- 东方财富条件单建议列表
- 一键复制 v8 完整报告

## 发布

1. 在 [微信公众平台](https://mp.weixin.qq.com/) 注册小程序并获取 AppID
2. 修改 `project.config.json` 中的 `appid` 字段
3. 在开发者工具中点击 **上传** → **提交审核**

## 核心逻辑

引擎位于 `utils/v7-core.js` + `utils/v8-core.js`，源文件在 `shared/js/`。

同步命令：

```bash
./scripts/sync_js.sh
```

## 免责声明

本小程序为结构概率决策演示工具，不构成投资建议。
