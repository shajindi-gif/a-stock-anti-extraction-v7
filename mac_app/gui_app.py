#!/usr/bin/env python3
"""A股反收割系统 v8 — macOS 桌面应用。"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont
from tkinter import ttk

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.demo_scenarios import get_scenario, list_scenarios  # noqa: E402
from engine_v8 import run_v8_pipeline  # noqa: E402

SCENARIO_LABELS = {
    "bullish_kcb50": "科创50ETF · 多头结构",
    "sideways_hs300": "沪深300ETF · 震荡结构",
    "bear_trap_detected": "创业板ETF · 诱多检测",
    "liquidity_crisis": "科创50ETF · 流动性危机",
}

COLORS = {
    "bg": "#0d1117",
    "panel": "#161b22",
    "border": "#30363d",
    "text": "#e6edf3",
    "muted": "#8b949e",
    "accent": "#58a6ff",
    "green": "#3fb950",
    "yellow": "#d29922",
    "red": "#f85149",
}


class AntiExtractionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("A股反收割系统 v8")
        self.geometry("760x820")
        self.minsize(640, 680)
        self.configure(bg=COLORS["bg"])

        self._setup_styles()
        self._build_ui()
        self._analyze("bullish_kcb50")

    def _setup_styles(self) -> None:
        self.option_add("*Font", "PingFang SC 13")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=COLORS["panel"],
            background=COLORS["panel"],
            foreground=COLORS["text"],
        )
        style.configure(
            "Run.TButton",
            background=COLORS["accent"],
            foreground="#ffffff",
            padding=(16, 8),
            font=("PingFang SC", 13, "bold"),
        )
        style.map("Run.TButton", background=[("active", "#1f6feb")])

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=COLORS["bg"], pady=12)
        header.pack(fill="x", padx=24)

        title_font = tkfont.Font(family="PingFang SC", size=20, weight="bold")
        tk.Label(
            header,
            text="🚀 A股反收割系统 v8",
            font=title_font,
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor="w")
        tk.Label(
            header,
            text="AI决策 + 执行闭环 + 东方财富条件单 · 选场景后点运行",
            font=("PingFang SC", 11),
            fg=COLORS["muted"],
            bg=COLORS["bg"],
        ).pack(anchor="w", pady=(4, 0))

        control = tk.Frame(self, bg=COLORS["panel"], padx=16, pady=12)
        control.pack(fill="x", padx=24, pady=(0, 8))

        tk.Label(control, text="Demo 场景", fg=COLORS["muted"], bg=COLORS["panel"]).pack(
            side="left", padx=(0, 8)
        )

        self.scenario_var = tk.StringVar(value="bullish_kcb50")
        combo = ttk.Combobox(
            control,
            textvariable=self.scenario_var,
            values=list_scenarios(),
            state="readonly",
            width=28,
        )
        combo.pack(side="left", padx=(0, 12))
        combo.bind("<<ComboboxSelected>>", self._on_scenario_change)

        ttk.Button(control, text="▶ 运行分析", style="Run.TButton", command=self._run).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(control, text="复制报告", command=self._copy_report).pack(side="left")

        self.prob_canvas = tk.Canvas(self, height=28, bg=COLORS["bg"], highlightthickness=0)
        self.prob_canvas.pack(fill="x", padx=24, pady=(0, 8))

        self.output = tk.Text(
            self,
            wrap="word",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            padx=16,
            pady=12,
            font=("Menlo", 11),
        )
        self.output.pack(fill="both", expand=True, padx=24, pady=(0, 8))
        self.output.configure(state="disabled")

        tk.Label(
            self,
            text="⚠️ 演示工具，不构成投资建议 · 条件单请在东财 APP 手动设置 · v8.0.0",
            fg=COLORS["muted"],
            bg=COLORS["bg"],
            font=("PingFang SC", 10),
        ).pack(pady=(0, 10))

    def _on_scenario_change(self, _event: object = None) -> None:
        self._analyze(self.scenario_var.get())

    def _run(self) -> None:
        self._analyze(self.scenario_var.get())

    def _analyze(self, scenario_name: str) -> None:
        result = run_v8_pipeline(get_scenario(scenario_name))
        self._draw_prob_bar(result.v7.probability)
        self._render_report(result.to_report())

    def _draw_prob_bar(self, prob: dict[str, float]) -> None:
        self.prob_canvas.delete("all")
        w = self.prob_canvas.winfo_width() or 640
        h = 28
        x = 0
        segments = [
            ("up", prob["up"], COLORS["green"], "上涨"),
            ("side", prob["side"], COLORS["yellow"], "震荡"),
            ("down", prob["down"], COLORS["red"], "下跌"),
        ]
        for _key, pct, color, label in segments:
            seg_w = w * pct
            if seg_w < 1:
                continue
            self.prob_canvas.create_rectangle(x, 0, x + seg_w, h, fill=color, outline="")
            if seg_w > 40:
                self.prob_canvas.create_text(
                    x + seg_w / 2,
                    h / 2,
                    text=f"{label} {pct:.0%}",
                    fill="#000000" if _key == "side" else "#ffffff",
                    font=("PingFang SC", 10, "bold"),
                )
            x += seg_w

    def _render_report(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")
        self._report_text = text

    def _copy_report(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(getattr(self, "_report_text", ""))
        self.title("A股反收割系统 v8 · 已复制 ✓")
        self.after(1500, lambda: self.title("A股反收割系统 v8"))


def main() -> None:
    app = AntiExtractionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
