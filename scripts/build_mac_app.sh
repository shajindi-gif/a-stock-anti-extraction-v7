#!/bin/bash
# 构建 macOS .app 应用包
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
APP_NAME="A股反收割系统v7"
BUILD_DIR="$PROJECT_DIR/dist"
APP_DIR="$BUILD_DIR/${APP_NAME}.app"

echo "🔨 构建 ${APP_NAME}.app ..."

rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# 检测 Python
PYTHON="$(command -v python3)"
echo "使用 Python: $PYTHON"

# 启动脚本
cat > "$APP_DIR/Contents/MacOS/launcher" << 'LAUNCHER'
#!/bin/bash
DIR="$(cd "$(dirname "$0")/../Resources" && pwd)"
cd "$DIR"
exec python3 mac_app/gui_app.py
LAUNCHER
chmod +x "$APP_DIR/Contents/MacOS/launcher"

# Info.plist
cat > "$APP_DIR/Contents/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.antiharvest.v7</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleDisplayName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleVersion</key>
    <string>7.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>7.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST

# 复制项目文件到 Resources
rsync -a \
    --exclude='dist' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    "$PROJECT_DIR/" "$APP_DIR/Contents/Resources/"

echo "✅ 构建完成: $APP_DIR"
echo ""
echo "启动方式:"
echo "  open \"$APP_DIR\""
echo "  或双击 Finder 中的 ${APP_NAME}.app"
