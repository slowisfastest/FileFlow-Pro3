# FileFlow Pro - Windows 部署包

## 📦 文件说明

```
convert_for_windows_v1/
├── fileflow_pro.py              # 主程序源代码
├── requirements.txt             # Python 依赖列表
├── build_windows.py             # 本地打包脚本（备用）
├── .github/
│   └── workflows/
│       └── build-windows.yml    # GitHub Actions 配置
├── GitHub Actions 打包说明.md   # 在线打包教程
├── Windows打包说明.md           # 本地打包教程
└── README.md                    # 本文件
```

## 🚀 推荐方案：GitHub Actions 在线打包

**优势**：完全不需要在 Windows 电脑上安装任何软件！

### 快速开始

1. **注册 GitHub 账号**（免费）
   - 访问 https://github.com/signup

2. **创建仓库**
   - 访问 https://github.com/new
   - 仓库名称：`fileflow-pro`
   - 点击 **Create repository**

3. **上传本文件夹所有内容**
   - 在仓库页面点击 **"uploading an existing file"**
   - 将整个 `convert_for_windows_v1` 文件夹内容拖进去
   - 点击 **Commit changes**

4. **触发打包**
   - 点击 **Actions** 标签
   - 选择 **"Build Windows EXE"**
   - 点击 **"Run workflow"** → **Run workflow**

5. **下载 EXE**
   - 等待 3-5 分钟
   - 在运行记录页面底部 **Artifacts** 区域
   - 点击 **FileFlowPro-Windows** 下载

详细步骤请查看 **GitHub Actions 打包说明.md**

## 💻 备用方案：本地打包

如果无法使用 GitHub，可以在 Windows 电脑上本地打包：

1. 安装 Python 3.8+（https://python.org）
2. 打开命令提示符，进入本文件夹
3. 运行：`python build_windows.py`
4. 等待打包完成，生成 `FileFlowPro.exe`

详细步骤请查看 **Windows打包说明.md**

## 📋 系统要求

- Windows 10 或 Windows 11
- 4GB 内存
- 500MB 可用磁盘空间

## ✨ 功能特性

- PDF 转 Word/Excel/PPT/图片/文本
- Word/Excel/PPT 转 PDF
- 图片格式转换（PNG/JPG/WebP）
- 文本转 PDF/Word

## 📝 注意事项

- GitHub Actions 打包完全免费
- 每次代码更新后，Actions 会自动重新打包
- 生成的 EXE 文件约 50-100MB（包含所有依赖）

## ❓ 需要帮助？

查看详细文档：
- `GitHub Actions 打包说明.md` - 在线打包详细教程
- `Windows打包说明.md` - 本地打包详细教程
