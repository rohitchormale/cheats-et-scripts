#!/bin/bash

# convert all video files from given dict to mp3 using ffmpeg

for i in *
do
  ffmpeg -i $i -f mp3 -ab 192000 -vn $i.mp3
done

