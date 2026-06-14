.PHONY: install start run run-v8 demo test gui build-app open-app web dashboard sync-js icons chrome clean

install:
	chmod +x scripts/install.sh scripts/start.sh scripts/serve_web.sh scripts/sync_js.sh
	./scripts/install.sh

start:
	chmod +x scripts/start.sh
	./scripts/start.sh

run:
	python3 run_v7.py

run-v8:
	python3 run_v8.py

demo:
	python3 demo/demo_cli.py --all

demo-interactive:
	python3 demo/demo_cli.py

gui:
	python3 mac_app/gui_app.py

test:
	python3 -m unittest tests.test_v7 tests.test_v8 -v

build-app:
	chmod +x scripts/build_mac_app.sh
	./scripts/build_mac_app.sh

open-app:
	open "dist/A股反收割系统v8.app"

web:
	chmod +x scripts/serve_web.sh
	./scripts/serve_web.sh

dashboard:
	streamlit run dashboard/streamlit_app.py

sync-js:
	chmod +x scripts/sync_js.sh
	./scripts/sync_js.sh

icons:
	python3 scripts/generate_icons.py

chrome: icons sync-js
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "Chrome 插件：chrome://extensions/"
	@echo "开发者模式 → 加载 chrome_extension/ 目录"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

clean:
	rm -rf dist/ build/ __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
