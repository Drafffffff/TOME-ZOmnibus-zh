-- Execute the shipped I18N implementation, not a replacement translator.
local root = assert(arg[1], 'project root required')
class = {make=function() end}
package.preload['engine.class'] = function() return class end
local chunk = assert(loadfile(root..'/upstream/I18N.lua'))
chunk('engine.I18N')
local I18N = assert(package.loaded['engine.I18N'])
fs={exists=function(p) local f=io.open(p);if f then f:close();return true end end}
util={loadfilemods=function(p,env) local f,e=loadfile(p);if f then setfenv(f,env) end;return f,e end}
config={settings={locale='zh_hans',tome={}}}
I18N:loadLocale(root..'/build/lite/data/locales/zh_hans.lua')
I18N:setLocale('zh_hans')
local cases=assert(loadfile(root..'/tests/cases.lua'))()
for _,c in ipairs(cases) do
  local got=c[1]:tformat(unpack(c[2]))
  assert(type(got)=='string' and #got>0, c[1])
end
local extract='There %s %d non-unique metallic item%s in your transmogrification chest.  Extract gem%s from %s?'
assert(extract:tformat('are',7,'s','s','them')=='转化箱中有7件非独特金属物品。是否从中提取宝石？')
assert(('Delete %d note%s?'):tformat(2,'s')=='删除2条笔记？')
assert(('%s (%sactivated) #LIGHT_GREEN#(%d,%d, est.dist. %.2f)#LAST#'):tformat('拉杆',_t'not ',1,2,3):find('未激活',1,true))
assert(_t('Semi-Roguelike (mild)','birth descriptor name')=='半永久死亡（微辣）')
I18N:setLocale('en_US')
assert(_t'Roguelike Keybindings'=='Roguelike Keybindings')
assert(extract:tformat('are',7,'s','s','them'):find('There are 7',1,true))
I18N:setLocale('zh_hans')
print('PASS: '..#cases..' translated format calls, argument reorder, birth names, English fallback')

-- Verify package loading after the game's bundled Simplified Chinese locale.
I18N:loadLocale(root..'/upstream/base-zh_hans.lua')
I18N:loadLocale(root..'/build/lite/data/locales/zh_hans.lua')
I18N:setLocale('zh_hans')
assert(extract:tformat('are',7,'s','s','them')=='转化箱中有7件非独特金属物品。是否从中提取宝石？')

-- Run actual option-generation hooks with UI shells, retaining the real text
-- and callbacks. Rendering and actor gameplay are not simulated here.
local function set(t,...)
 local args={...};local val=table.remove(args)
 for i=1,#args-1 do t[args[i]]=t[args[i]] or {};t=t[args[i]] end
 t[args[#args]]=val
end
table.set=set
table.get=function(t,...)
 for _,k in ipairs({...}) do if type(t)~='table' or t[k]==nil then return nil,false end;t=t[k] end
 return t,true
end
table.getTable=function(t,...) local v,ok=table.get(t,...);if not ok then table.set(t,...,{});return table.get(t,...) end;return v end
string.toTString=function(s)return s end
function string:capitalize() return self end
function string:toTString() return self end
local hooks={}
class.bindHook=function(_,name,f) hooks[name]=hooks[name] or {};table.insert(hooks[name],f) end
package.preload['mod.dialogs.UseItemMnemonicConfig']=function()return {optDesc=function()return '已配置' end} end
local shell={new=function(t)t.getDisplayString=function()return '[图标]' end;return t end}
package.preload['engine.Birther']=function()return {loadDefinition=function()end} end
package.preload['mod.class.interface.WorldAchievements']=function()return {loadDefinition=function()end} end
package.preload['engine.ui.Textzone']=function()return shell end
package.preload['engine.ui.Dialog']=function()return {} end
package.preload['engine.KeyBind']=function()return {} end
package.preload['engine.interface.ActorTalents']=function()return {talents_def={}} end
package.preload['engine.interface.ActorTemporaryEffects']=function()return {loadDefinition=function()end} end
package.preload['engine.Entity']=function()return shell end
local original_dofile=dofile
dofile=function(path)
 local mapped=path:gsub('^/hooks/zomnibus_lite/',root..'/build/lite/hooks/')
 return original_dofile(mapped)
end
original_dofile(root..'/build/lite/hooks/load.lua')
profile={mod={allow_build={birth_transmo_chest=true}}}
game={isAddonActive=function()return false end}
local dlg={c_desc={w=900,h=900}}
local data={list={zomnibus_options=true}}
dlg.list=data.list
for _,f in ipairs(hooks['GameOptions:generateList'])do f(dlg,data) end
local count=0
for _,item in ipairs(data.list)do
 assert(type(item.name)=='string' and item.name:find('[\128-\255]'), 'untranslated option: '..tostring(item.name))
 if item.zone then assert(item.zone.text:find('[\128-\255]'),item.zone.text) end
 if item.status then assert(type(item.status(item))=='string',item.name) end
 count=count+1
end
assert(count>=40,'missing options')
print('PASS: generated '..count..' real option rows with Chinese descriptions and working status callbacks')
