import cv2
file_path = "/Users/eugeneyu/work/gcp/products/TranscoderAPI/oasis/source.mkv"  # change to your own video path
vid = cv2.VideoCapture(file_path)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

print(f"height: {height}")
print(f"width: {width}")

target_width = 720
target_aspect_ratio_reverse = 3/4