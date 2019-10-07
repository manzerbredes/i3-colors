#!/bin/bash

##### Requirements #####
# - scrot
# - imagemagick
################## #####

wai=$(dirname $(readlink -f $0))
theme_loc="${wai}/../themes/"
i3_colors="${wai}/../src/i3-colors.py"

echo "Get ready for screenshots (5s)..."
sleep 5
for theme in $(ls ${theme_loc}|grep -v ".jpg")
do
    $i3_colors -r ${theme_loc}/${theme}
    sleep 2 # Wait for i3 reload
    scrot ${wai}/${theme}.png
done


for shot in ${wai}/*.png
do
    x=$(identify $shot|awk '{print $3}'|cut -dx -f1)
    y=52 # Please change according to your resolution
    convert $shot -crop ${x}x${y} output_tmp.jpg
    mv output_tmp-0.jpg $(basename $shot|sed "s/.png/.jpg/g")
    rm ${shot}
done

rm ${wai}/output_tmp*.jpg



