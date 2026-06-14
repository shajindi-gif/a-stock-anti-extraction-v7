# Streamlit 数据看板

```bash
# 安装依赖（首次）
pip install streamlit pandas

# 启动看板
make dashboard
# 或
streamlit run dashboard/streamlit_app.py
```

浏览器自动打开 **http://localhost:8501**

## 看板功能

| Tab | 内容 |
|-----|------|
| 决策概览 | 概率预测、结构判断、风控 |
| 执行闭环 | 订单路由、仓位重平衡、自动止损 |
| 东财条件单 | 条件单列表 + 操作路径 + 可复制指南 |
| 全场景对比 | 4 场景数据表 + 概率对比图 |

## 侧边栏

- Demo 场景切换
- 组合总值 adjustable（影响重平衡计算）
