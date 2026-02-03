# 广州理工学院教务系统自动登录脚本

## 项目简介
基于Selenium的教务系统自动登录脚本，支持广州理工学院教务系统自动化登录，包含验证码自动识别功能。

## 快速开始

### 1. 下载项目

**方式一：Git 克隆**
```bash
git clone https://github.com/zonalet68/1.git
cd 广州理工学院教务系统自动化登录
```

**方式二：下载压缩包**
1. 访问项目页面下载 ZIP 压缩包
2. 解压到本地目录

### 2. 安装依赖

**⚠️ 重要：以下命令需要在命令行中执行，不是在Python代码中运行！**

**方式一：使用 requirements.txt 安装（推荐）**
```bash
pip install -r requirements.txt
```

**方式二：逐个安装（使用清华镜像源）**
```bash
pip install selenium>=4.15.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install ddddocr>=1.4.8 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install Pillow>=9.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests>=2.28.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**详细安装说明：** 查看 `依赖包下载文本.txt` 文件

**系统要求：**
- Python 3.7+
- Microsoft Edge 浏览器

### 3. 配置账号

**方式一：手动输入（首次推荐）**

首次使用时，直接双击 `start.bat`，程序会提示输入学号、密码和登录URL。输入完成后，程序会自动保存到 `config.json` 文件中，下次运行无需再次输入。

**方式二：编辑配置文件**

直接编辑 `config.json` 文件，修改以下内容：

| 字段 | 说明 | 示例 |
|------|------|------|
| username | 学号 | `"202012345"` |
| password | 密码 | `"your_password"` |
| loginUrl | 登录网址 | `"http://jw.gzist.edu.cn/jwglxt/xtgl/login_slogin.html"` |

**示例：**
```json
{
  "username": "202012345",
  "password": "your_password",
  "loginUrl": "http://jw.gzist.edu.cn/jwglxt/xtgl/login_slogin.html"
}
```

**⚠️ 注意：密码以明文存储，请注意文件安全**

### 4. 运行程序

**Windows:** 双击 `start.bat` 或运行 `python jw.py`
**macOS/Linux:** 运行 `python jw.py`

## 功能特点
- 🔧 自动识别学号和密码输入框
- 🤖 基于ddddocr的验证码自动识别
- 🎯 智能填写表单并触发JavaScript事件
- 🖱️ 支持手动干预模式
- ✅ 自动配置检测，未配置时切换到手动输入
- 🐛 详细的调试信息输出

## 使用方法

### 方式一：双击 `start.bat`（推荐）

### 方式二：运行 `python jw.py`

### 运行流程
1. 检查配置文件
2. 打开浏览器访问登录页面
3. 填写学号和密码
4. 识别并填写验证码（最多尝试3次）
5. 点击登录按钮
6. 登录成功后保持浏览器打开

### 手动输入模式
如果 `config.json` 未配置，程序会提示输入学号、密码和登录URL。

## 特色功能

### 智能识别
- 自动识别学号、密码、验证码输入框
- 基于ddddocr深度学习模型识别验证码
- 最多自动尝试3次识别

### 灵活配置
- 自动检测配置文件
- 无配置时切换到手动输入模式

## 注意事项

1. ⚠️ 首次使用前必须执行 `pip install -r requirements.txt`
2. 🔐 配置文件密码为明文存储，请注意安全
3. 🌐 确保能正常访问教务系统
4. 🖥️ 建议使用Windows系统配合Edge浏览器
5. ⏰ 验证码识别可能失败，需手动输入

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| ModuleNotFoundError | 执行 `pip install -r requirements.txt` |
| 'pip' 不是内部或外部命令 | 重装Python并勾选 "Add Python to PATH" |
| 下载速度慢 | 使用镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` |
| ddddocr 安装失败 | `pip install setuptools wheel` 后再安装 ddddocr |
| 浏览器无法启动 | 安装Microsoft Edge浏览器 |
| 验证码识别失败 | 手动输入验证码 |
| 登录失败 | 检查账号密码和验证码是否正确 |

## 文件说明

- `jw.py` - 主程序
- `config.json` - 配置文件（可选）
- `start.bat` - Windows启动脚本
- `requirements.txt` - Python依赖包列表
- `依赖包下载文本.txt` - 依赖包详细安装说明
- `README.md` - 本文档
- `msedgedriver.exe` - Edge浏览器驱动

## 技术栈
- Python 3.x
- Selenium WebDriver
- ddddocr
- Microsoft Edge WebDriver
- JavaScript DOM操作

## 版本历史
- v1.0 - 初始版本
- v1.1 - 添加ddddocr验证码识别
- v2.0 - 添加自动配置检测和手动输入模式
- v2.1 - 更新文档，简化说明

## 免责声明
本脚本仅供学习交流使用，请遵守学校相关规定。因使用本脚本造成的任何问题，作者不承担责任。

