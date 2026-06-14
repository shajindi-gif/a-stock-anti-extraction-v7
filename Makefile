.PHONY: run demo test app build-app open-app web sync-js icons chrome clean

run:
	python3 run_v7.py

demo:
	python3 demo/demo_cli.py --all

demo-interactive:
	python3 demo/demo_cli.py

gui:
	python3 mac_app/gui_app.py

test:
	python3 -m unittest tests.test_v7 -v

build-app:
	chmod +x scripts/build_mac_app.sh
	./scripts/build_mac_app.sh

open-app:
	open "dist/A股反收割系统v7.app"

web:
	chmod +x scripts/serve_web.sh
	./scripts/serve_web.sh

sync-js:
	chmod +x scripts/sync_js.sh
	./scripts/sync_js.sh

icons:
	python3 scripts/generate_icons.py

chrome: icons sync-js
	@echo "请在 Chrome 打开 chrome://extensions/ 加载 chrome_extension/ 目录"

clean:
	rm -rf dist/ build/ __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
