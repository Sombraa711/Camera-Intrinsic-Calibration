
### Install
``` 
pip install opencv-python
pip install numpy
pip install pycolmap
```

### extract_frames usage
```
1. prepare a video
2. python3 extract_frames.py --video /path/to/your_video --out /path/to/output --fps 30
```

### camera_parameter_generate usage
``` usage
# 1. Prepare some continuous images from the camera (by using extract_frames.py). (Option: use webcam id, it would extract frames within 3s automatically)
# 2. python3 camera_parameter_generate.py --source 0
# 2. python3 camera_parameter_generate.py --source /path/to/images
```
