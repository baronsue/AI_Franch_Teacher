#!/bin/bash

# AI法语老师 - 启动脚本 (Linux/Mac)

echo "========================================="
echo "  🎓 AI法语老师 - French Teacher"
echo "========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "📥 检查并安装依赖..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ 依赖安装完成"
echo ""

# 创建必要的目录
mkdir -p logs
mkdir -p data

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到.env文件"
    echo "   如需使用真实API，请复制 .env.example 为 .env 并配置"
    echo ""
fi

# 启动应用
echo "========================================="
echo "🚀 启动AI法语老师服务..."
echo "========================================="
echo ""
echo "📍 访问地址: http://localhost:5000"
echo "📍 API健康检查: http://localhost:5000/api/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd backend
python3 app.py
