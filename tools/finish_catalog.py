import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'translations.json'; d=json.loads(p.read_text()); keys=list(json.loads((root/'strings.json').read_text()))
s=keys[241]
a,b=s.split('The affected keybindings are:\n',1)
a='将此选项从“未安装”切换为“已安装”，会把移动键改为传统 Roguelike／Vi 布局，适合笔记本和没有数字小键盘的键盘。切换回“未安装”会恢复受影响按键的默认绑定。\n      \n#YELLOW##{italic}#[注意：“已安装／未安装”状态仅供参考；切换此设置时才会实际修改按键绑定。]#{normal}##LAST#\n\n受影响的按键如下：\n'
repl={'Move left:':'向左移动：','Move right:':'向右移动：','Move up:':'向上移动：','Move down:':'向下移动：','Move diagonally left and up:':'向左上移动：','Move diagonally right and up:':'向右上移动：','Move diagonally left and down:':'向左下移动：','Move diagonally right and down:':'向右下移动：','Stay for a turn:':'等待一回合：','Run left:':'向左连续移动：','Run right:':'向右连续移动：','Run up:':'向上连续移动：','Run down:':'向下连续移动：','Run diagonally left and up:':'向左上连续移动：','Run diagonally right and up:':'向右上连续移动：','Run diagonally left and down:':'向左下连续移动：','Run diagonally right and down:':'向右下连续移动：','Attack left:':'向左攻击：','Attack right:':'向右攻击：','Attack up:':'向上攻击：','Attack down:':'向下攻击：','Attack diagonally left and up:':'向左上攻击：','Attack diagonally right and up:':'向右上攻击：','Attack diagonally left and down:':'向左下攻击：','Attack diagonally right and down:':'向右下攻击：','Show message log:':'显示消息日志：','Show quests:':'显示任务：','Look around:':'查看周围：','Use items:':'使用物品：','Toggle movement mode:':'切换移动模式：','Show Lua console:':'显示 Lua 控制台：','Lock tooltip in place:':'锁定浮窗位置：','Lock tooltip in place while comparing items:':'对比物品时锁定浮窗位置：','Comma':'逗号','Keypad':'数字小键盘','(RL)':'（传统）','(dflt)':'（默认）',' vs. ':' ／ '}
for x,y in repl.items():b=b.replace(x,y)
d[s]=a+b
# These are additional UI strings that were not caught by literal _t/tformat extraction.
extra={
'Honorary Roguelike Win':'荣誉永久死亡胜利',
'Going to Landmark':'前往地标',
'how are you seeing this?':'你是怎么见到这条信息的？',
'#GOLD##{bold}#Sort inventory by pickup time#LAST##{normal}#':'#GOLD##{bold}#按拾取时间排列背包#LAST##{normal}#',
'#GOLD##{bold}#Sort weapons by damage#LAST##{normal}#':'#GOLD##{bold}#按伤害排列武器#LAST##{normal}#',
'Select a Tile':'选择外观图块',
'Use default tile':'使用默认外观',
'Zone orbs have been repaired and reset.  We Apologize for the Inconvenience.':'已修复并重置区域中的水晶球。给你带来不便，敬请谅解。',
'Select sort option':'选择排序方式',
'Use as sentry':'用作哨兵',
'You create: %s':'你制造了：%s',
'%s telekinetically seizes: %s.':'%s用念力抓取了：%s。',
'#YELLOW#Options provided by the %s addon, standalone or as a component of ZOmnibus or ZOmnibus Lite.#LAST#':'#YELLOW#以下选项由“%s”插件提供，可单独使用，也包含在 ZOmnibus 完整版或 Lite 中。#LAST#',
'#YELLOW#Options provided by the %s addon, standalone or as a component of ZOmnibus.#LAST#':'#YELLOW#以下选项由“%s”插件提供，可单独使用，也包含在 ZOmnibus 完整版中。#LAST#',
'ZOmnibus Lite':'ZOmnibus Lite（简体中文）',
'The cosmetic/informational/UI addons from ZOmnibus.':'ZOmnibus 的外观、信息与界面优化插件合集。附带完整简体中文译文。',
'Lichform':'巫妖形态',
'Talent points to invest in Lichform: ':'投入巫妖形态的技能点：',
'#LIGHT_BLUE#(including free point for completing the "From Death, Life" quest)#LAST#':'#LIGHT_BLUE#（包含完成“由死而生”任务获得的免费点数）#LAST#',
'#YELLOW#You have spent a category point in Spell/Necrosis#LAST#':'#YELLOW#你已在法术／死灵技能系中投入一个技能系点数#LAST#',
'Spend category point in Spell/Necrosis':'在法术／死灵技能系中投入技能系点数',
', for Celestial/Star Fury x%.1f':'，天界／星怒精通度 x%.1f',
'#LIGHT_BLUE#Resultant Lichform talent level %.1f%s#LAST#':'#LIGHT_BLUE#最终巫妖形态技能等级 %.1f%s#LAST#',
'Low Lichform TL':'巫妖形态等级不足',
'The specified configuration will not gain Celestial/Star Fury.':'当前配置无法获得天界／星怒技能系。',
'Planner clone level:':'规划副本等级：',
'Include ':'包含',
'Occult Technomancy':'神秘科技法术',
'Galvanic Technomancy':'电流科技法术',
'Terrene Technomancy':'大地科技法术',
'Mark As Seen':'标记为已见过',
'Delete note?':'删除笔记？',
'No':'否',
'Yes':'是',
'You extract %s from %s':'你提取出%s，来源：%s',
'??? tooltip() method missing':'未知：缺少 tooltip() 方法',
'#AQUAMARINE#You have gained one more life (%d remaining).#LAST#':'#AQUAMARINE#你获得了一次额外生命（剩余%d次）。#LAST#',
'#AQUAMARINE#Gained life! (%d remaining)#LAST#':'#AQUAMARINE#获得额外生命！（剩余%d次）#LAST#',
'You currently have %d saved %s points.  Special level-up markers will be used for these saved points, so you can tell when you have new points beyond those to spend.':'你当前标记保留了%d个%s。升级提示会使用特殊标记，让你区分保留点数与新获得的可分配点数。',
'Press this button to save your %d current %s points; press it again to reset your saved %s point level to zero.':'按此按钮可将当前%d个%s标记为保留；再次按下可将保留的%s数量重置为零。',
'Press this button to reset your saved %s point level to zero.':'按此按钮可将保留的%s数量重置为零。',
'Press this button to save your unused %s points (when you have some); press it again to reset your saved %s point level to zero.':'有未分配的%s时，按此按钮可将其标记为保留；再次按下可将保留的%s数量重置为零。',
'%s picks up (%s.): %s%s.':'%s拾取（%s）：%s%s。',
'%s has no room for: %s.':'%s没有空间容纳：%s。',
'There is nothing to pick up there.':'那里没有可拾取的物品。',
'[ZOmnibus]':'[ZOmnibus]',
}
for a,b in [('mild','微辣'),('barbecue','烧烤味'),('sweet&sour','酸甜味'),('spicy','辛辣'),('szechuan','川辣'),('vanilla','香草味'),('habañero','哈瓦那椒'),('ghost pepper','魔鬼椒'),('dark chocolate','黑巧克力'),('haggis','羊杂布丁')]:extra[f'Semi-Roguelike ({a})']=f'半永久死亡（{b}）'
d.update(extra)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(root/'extra_strings.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
print(len(d),'translations')
