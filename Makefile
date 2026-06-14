.PHONY: run demo test app build-app clean

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

clean:
	rm -rf dist/ build/ __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
