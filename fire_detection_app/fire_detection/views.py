from django.shortcuts import render
import cv2
import numpy as np
from django.conf import settings
import os
from . forms import FileUploads

# Create your views here.

def detect_fire(frame):
    ray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)
    _, thresholded_frame = cv2.threshold(blurred_frame, 50, 255, cv2.THRESH_BINARY)
    fire_pixel_count = np.sum(thresholded_frame == 255)
    frame_size = frame.shape[0] * frame.shape[1]
    fire_percentage = (fire_pixel_count / frame_size) * 100.0
    return fire_percentage
def fire_detection(request):
    form=FileUploads()
    frame_message = ""
    image_message = ""
    fire_percentage=0
    if request.method=="POST":
        form=FileUploads(request.POST,request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            image_file = form.cleaned_data['image_file']
            form.save()
            video_path = os.path.join(settings.MEDIA_ROOT,  video_file.name)
            cap = cv2.VideoCapture(video_path)
            image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
            # image_path = image_file.name
            image = cv2.imread(image_path)

            frame_display_width = 640
            frame_display_height = 480
            image_display_width = 640
            image_display_height = 480

            cv2.namedWindow('Fire Detection', cv2.WINDOW_NORMAL)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (frame_display_width, frame_display_height))
                fire_percentage = detect_fire(frame)

                image_copy = image.copy()
                image_copy = cv2.resize(image_copy, (image_display_width, image_display_height))
                image_fire_percentage = detect_fire(image_copy)

                combined_frame = np.zeros((frame_display_height, frame_display_width * 2, 3), dtype=np.uint8)
                combined_frame[:, :frame_display_width, :] = frame
                combined_frame[:, frame_display_width:, :] = image_copy

                if fire_percentage >= 80:
                    frame_message = f'Fire Detected: {fire_percentage:.2f}%'
                    frame_color = (0, 0, 255)
                else:
                    frame_message = f'Fire Not Detected: {fire_percentage:.2f}%'
                    frame_color = (0, 255, 0)

                if image_fire_percentage >= 80:
                    image_message = f'Fire Detected: {image_fire_percentage:.2f}%'
                    image_color = (0, 0, 255)
                else:
                    image_message = f'Fire Not Detected: {image_fire_percentage:.2f}%'
                    image_color = (0, 255, 0)

                cv2.putText(combined_frame, frame_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, frame_color, 2)
                cv2.putText(combined_frame, image_message, (frame_display_width + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, image_color, 2)

                cv2.imshow('Fire Detection', combined_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            return render(request,'fire_percentage.html',{'frame_message':frame_message,'image_message':image_message,'fire_percentage':fire_percentage})
            cap.release()
            cv2.destroyAllWindows()

    return render(request, 'fire_detection.html',{'form':form,'frame_message':frame_message,'image_message':image_message,'fire_percentage':fire_percentage})




