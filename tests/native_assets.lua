-- Run with the shipped native engine in an isolated Xvfb test directory.
fs.mount("/tmp/tome-zomnibus-fixed-zh.teaa", "/fixed-assets", true)
local names = {
"overload/data/gfx/achievements/exploration_sort_of_roguelike.png",
"overload/data/gfx/achievements/insane_adventure_sort_of_roguelike.png",
"overload/data/gfx/achievements/insane_sort_of_roguelike.png",
"overload/data/gfx/achievements/madness_adventure_sort_of_roguelike.png",
"overload/data/gfx/achievements/madness_sort_of_roguelike.png",
"overload/data/gfx/achievements/nightmare_adventure_sort_of_roguelike.png",
"overload/data/gfx/achievements/nightmare_sort_of_roguelike.png",
"overload/data/gfx/achievements/normal_roguelike_sort_of_roguelike.png",
"overload/data/gfx/achievements/sort_of_roguelike.png",
"overload/data/gfx/dark-ui/minimalist/party-portrait-lev-save.png",
"overload/data/gfx/dark-ui/minimalist/party-portrait-unselect-lev-save.png",
"overload/data/gfx/dark-ui/minimalist/playerframe/exp_back.png",
"overload/data/gfx/dark-ui/minimalist/playerframe/saved.png",
"overload/data/gfx/dark-ui/radio-ok.png",
"overload/data/gfx/dark-ui/radio.png",
"overload/data/gfx/effects/going_to_landmark.png",
"overload/data/gfx/landmark.png",
"overload/data/gfx/metal-ui/radio-ok.png",
"overload/data/gfx/metal-ui/radio.png",
"overload/data/gfx/simple-ui/radio-ok.png",
"overload/data/gfx/simple-ui/radio.png",
"overload/data/gfx/stone-ui/radio-ok.png",
"overload/data/gfx/stone-ui/radio.png",
"overload/data/gfx/ui/party-portrait-lev-save.png",
"overload/data/gfx/ui/party-portrait-unselect-lev-save.png",
"overload/data/gfx/ui/playerframe/exp_back.png",
"overload/data/gfx/ui/playerframe/saved.png",
"overload/data/gfx/unwielded-marker.png",
"overload/data/gfx/wishlist-mark-ego.png",
"overload/data/gfx/wishlist-mark-flag.png",
"overload/data/gfx/wishlist-mark-item.png",
}
for _,name in ipairs(names) do
 local img=assert(core.display.loadImage("/fixed-assets/"..name),name)
 local texture={img:glTexture()}
 assert(texture[1],name)
end
print("ASSET-FIX-PASS",#names,"PNG images loaded and converted to textures")
os.exit(0)
