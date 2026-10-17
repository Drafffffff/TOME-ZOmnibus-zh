# ZOmnibus Lite 简体中文补丁

针对用户实际安装的 **ZOmnibus Lite 17.9.5**，适配 ToME 1.7.6。不是 ZOmnibus 完整版的汉化包。

包含 792 条译文：设置及说明、背包和物品操作、商店心愿单与属性筛选、角色笔记、存档备注、地标、技能加点规划器、被动冷却提示、护盾提示、半永久死亡模式和成就、错误和兼容性提示。键名、插件品牌名、Lua 方法名等必要技术名称保留原文；其他第三方插件的内容仍由各自译文决定。

使用原生 `data/locales/zh_hans.lua`，并为缺少翻译接口的显示文字补充 `_t()`。保留原插件的 short_name、版本、内部配置键、出生描述符 ID、按键命令和游戏机制。中文仅在游戏语言为简体中文时启用；英文语言仍显示原文。已有加载 ZOmnibus Lite 的角色可直接使用，无需再次新建角色。

## 使用

已经安装到 Bazzite：

```
/home/bazzite/.local/share/Steam/steamapps/common/TalesMajEyal/game/addons/tome-zomnibus_lite.teaa
```

保存当前进度，完全退出游戏，然后重新启动。进入角色后按 Esc → 游戏选项 → `[ZOmnibus]`。HHKB 对应的选项现在显示为“传统 Roguelike 键位”。

原版备份位于：

```
/home/bazzite/.local/share/tome-mod-backups/zomnibus-lite-17.9.5-original.teaa
```

本地成品在 `dist/tome-zomnibus_lite.teaa`，它替换原包；不要同时保留两个不同文件名的 Lite 包。

创意工坊更新可能覆盖此文件。相同版本可重新安装本地成品；版本更新后应重新核对源文件再适配。请不要直接用本包覆盖未来不同版本。

恢复原版：退出游戏后，将上述备份复制回插件路径。恢复不需要修改存档。

## 验证

- 提取并逐一翻译 734 条原有静态翻译字符串，补齐其他显示文字，共 792 条。
- 71 个 Lua 文件均通过本机和 Bazzite 的 LuaJIT 编译。
- 使用游戏原版 `engine.I18N` 执行全部译文格式化，验证数字、占位符和去除英文复数词尾的参数重排。
- 通过实际设置钩子生成 52 行设置及子标题，检查中文说明和状态回调；加载游戏自带中文词库后再次检查。
- 全部颜色与字体标记保持一致。
- 尚未重启用户正在运行的游戏，因此没有声称完成游戏内视觉验收或逐个功能的实玩验证。

构建：

```
python3 tools/build.py
/opt/homebrew/bin/luajit tests/check.lua "$PWD"
```

源文提取脚本为 `tools/catalog.py`。`translations.json` 为人工译文；`catalog.json` 保存原字符串出现位置。`dist/validation.json` 保存编译、覆盖范围和校验和报告。上游原版包保存在 `upstream/`。

原插件作者：Scott Bigham（Zizzo）。保留原始版权声明，源代码及本翻译按 GPL-3.0-or-later 分发。

## 读档报错修复

首版中文包将资源压缩为 ZIP_DEFLATED，原生引擎加载 PNG 时返回空值，导致 `Minimalist.lua:42` 在读取 `playerframe/saved.png` 时出错。已用独立 Xvfb 环境中的游戏原生引擎复现：原包图片可加载，压缩包同一图片报告 `Not a PNG file`。

修正版保留上游 ZIP 条目的原始压缩方式及元数据；31 张 PNG 均通过原生引擎读取与 OpenGL 纹理转换验证。修复只替换插件包，不修改角色存档。完全退出并重启游戏后生效。
