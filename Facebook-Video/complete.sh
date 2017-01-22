blender -b William.blend -a
ffmpeg -r 24 -f image2 -s 1920x1080 -i %04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p wood.mp4
python post.py
