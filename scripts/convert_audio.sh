ffmpeg -i $1 -ar 44100 -codec:a:0 wmav2 -b:a 320000 out.wma
