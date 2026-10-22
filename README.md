# dhwgithub 仓库导航页

展示 [dhwgithub](https://github.com/dhwgithub) 全部公开仓库的单文件静态页面，托管在 GitHub Pages。

## 功能

- 点击卡片直接跳转对应 GitHub 仓库
- 搜索（名称 / 描述 / 标签 / 语言）
- 语言筛选、排序（更新时间 / Star / 名称 / 创建时间 / 体积）
- Fork 隐藏开关、网格 / 列表视图切换、深浅主题（跟随系统，可手动切换）
- 「同步」按钮：浏览器直接调 GitHub API 刷新数据（未认证限额 60 次/小时）
- 每周日由 GitHub Actions 自动拉取最新仓库列表并提交（见 `.github/workflows/sync.yml`）

## 结构

```
index.html   页面本体（数据内联，单文件，无外部依赖）
sync.py      数据同步脚本（Actions 调用，也可手动运行）
.nojekyll    禁用 Jekyll 处理
```

## 本地更新数据

```bash
python sync.py dhwgithub index.html
```
