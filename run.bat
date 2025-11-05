@echo off
REM AI法语老师 - 启动脚本 (Windows)

echo =========================================
echo   AI法语老师 - French Teacher
echo =========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo Python版本:
python --version
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装/更新依赖
echo 检查并安装依赖...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo 依赖安装完成
echo.

REM 创建必要的目录
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM 检查环境变量文件
if not exist ".env" (
    echo 警告: 未找到.env文件
    echo 如需使用真实API，请复制 .env.example 为 .env 并配置
    echo.
)

REM 启动应用
echo =========================================
echo 启动AI法语老师服务...
echo =========================================
echo.
echo 访问地址: http://localhost:5000
echo API健康检查: http://localhost:5000/api/health
echo.
echo 按 Ctrl+C 停止服务
echo.

cd backend
python app.py

pause
