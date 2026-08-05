#!/bin/sh
# QA captures. Edge headless --virtual-time-budget does NOT advance CSS
# animations, so the two animated states are driven deterministically:
#   mid-flight  -> ?stage=flight  (v2.js adds html.df-freeze: negative
#                  animation-delay + animation-play-state:paused, seeking the
#                  curtain wipe and the dragonfly to t=1.05s and holding there)
#   settled     -> --force-prefers-reduced-motion (renders the finished hero,
#                  identical to the post-entrance state; entrance nodes removed)
E="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
BASE="http://127.0.0.1:$1"
OUT="$PWD/qa-shots"
P="$PWD/_edgeprof"
shot(){ # name width height url extra
  "$E" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
       --user-data-dir="$P" --window-size="$2,$3" \
       --screenshot="$OUT/$1.png" --virtual-time-budget=4000 $5 "$4" >/dev/null 2>&1
  echo "  $1.png"
}
for w in 1280 492; do
  shot "home-entrance-start-$w"  $w 900  "$BASE/index.html?stage=flight"
  shot "home-settled-$w"         $w 900  "$BASE/index.html" --force-prefers-reduced-motion
  shot "detox-condensed-$w"      $w 3400 "$BASE/naturopathic-homeopathic-detox.html" --force-prefers-reduced-motion
  shot "about-full-portrait-$w"  $w 1200 "$BASE/about-lynette-wing-renewal-health.html" --force-prefers-reduced-motion
  shot "testimonials-$w"         $w 1500 "$BASE/testimonials.html" --force-prefers-reduced-motion
done
shot "gut-health-cards-1280"   1280 3200 "$BASE/gut-health-support.html" --force-prefers-reduced-motion
shot "programs-cards-1280"     1280 2600 "$BASE/programs-packages.html" --force-prefers-reduced-motion
shot "inflammation-1280"       1280 2800 "$BASE/inflammation-support.html" --force-prefers-reduced-motion
shot "home-full-1280"          1280 4400 "$BASE/index.html" --force-prefers-reduced-motion
