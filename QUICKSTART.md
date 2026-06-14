# 快速上手（3 分钟）

> 零基础也能用。不需要懂编程。

---

## 第一步：安装（只需一次）

**macOS / Linux：**

```bash
git clone https://github.com/shajindi-gif/a-stock-anti-extraction-v7.git
cd a-stock-anti-extraction-v7
./scripts/install.sh
```

或：

```bash
make install
```

**Windows：** 安装 [Python 3.9+](https://www.python.org/downloads/) 后，在项目目录执行：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run_v8.py
```

---

## 第二步：选一种方式使用

| 我想… | 命令 | 适合谁 |
|--------|------|--------|
| **菜单选择** | `make start` | 所有人（推荐） |
| **终端看报告** | `make run-v8` | 命令行用户 |
| **可视化看板** | `make dashboard` | 喜欢看图表 |
| **网页版** | `make web` → 打开 http://localhost:8080/web/ | 浏览器用户 |
| **Mac 桌面** | `make gui` | Mac 用户 |
| **在线 Web** | 打开 [在线演示](https://shajindi-gif.github.io/a-stock-anti-extraction-v7/) | 无需安装 |

---

## 第三步：看懂结果

1. **AI 决策** — BUY_TREND（买）/ HOLD（观望）/ NO_TRADE（禁止交易）
2. **仓位建议** — 建议持仓比例（如 70%）
3. **东财条件单** — 复制参数，到东方财富 APP 手动设置
4. **免责声明** — 演示工具，不构成投资建议

---

## 其他端

### Chrome 浏览器插件

1. 打开 `chrome://extensions/`
2. 开启「开发者模式」
3. 加载 `chrome_extension/` 文件夹

### 微信小程序

1. 下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 导入 `miniprogram/` 目录
3. AppID 选「测试号」

### Mac 独立应用

```bash
make build-app
make open-app
```

---

## 常见问题

**需要开户 / API Key 吗？**  
不需要。全部是 Demo 模拟数据。

**会自动帮我下单吗？**  
不会。条件单需要你在东方财富 APP 里手动设置。

**遇到问题？**  
运行 `make test` 检查是否正常（应显示 20 tests OK）。

---

更多细节见 [README.md](README.md)
