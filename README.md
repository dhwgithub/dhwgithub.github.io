# dhwgithub 产品发布中心

展示独立开发软件产品的发布页，完全托管在 GitHub 上（Pages + Releases），无任何自有服务器。

访问地址：<https://dhwgithub.github.io>

## 功能

- **产品展示**：卡片列表、搜索、排序（最新发布 / 下载最多 / 名称）
- **文件下载**：安装包与说明文件存放在 GitHub Release（单文件最大 2 GB），任何人无需登录即可直链下载，含实时下载计数
- **产品详情**：说明（链接自动识别）、源码 / 主页链接、文件列表（类型徽标、大小、单文件下载量、补充说明）
- **评论**：基于 giscus（GitHub Discussions），GitHub 用户可评论、回复、点赞，支持邮件通知
- **管理后台**：仅 `dhwgithub` 可用，浏览器内直接发布 / 编辑 / 下架 / 删除产品，上传带进度条
- 深浅主题（跟随系统，可手动切换，评论主题同步）

## 架构

```
index.html          单文件前端（无构建、无外部 JS 依赖，评论除外）
data/products.json  产品元数据（管理后台通过 GitHub Contents API 提交）
Releases/           产品文件（安装包等，由后台通过 Releases API 上传）
Discussions/        评论数据（giscus）
```

## 管理员使用

1. 打开站点，点右上角「管理」
2. 粘贴一个 Fine-grained Token 登录（创建入口：GitHub Settings → Personal access tokens → Fine-grained；Repository access 选 Only select repositories → 本仓库；权限只需 Contents: Read and write）
3. 填写产品信息并选择文件，点「发布」

注意事项：

- GitHub Release 资产不支持中文文件名，后台会自动改用安全文件名上传，页面显示名不受影响
- 发布 / 修改后，GitHub Pages 约 1 分钟内刷新
- giscus 评论按产品名称关联讨论，产品发布后请勿改名
- Token 仅保存在管理员自己浏览器的 localStorage，直连 GitHub API
