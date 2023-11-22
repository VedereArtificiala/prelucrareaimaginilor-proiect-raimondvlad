import cv2

image_path = "Test images/TestImage.jpg"
image = cv2.imread(image_path)



# resizing the image
desired_width = 1280
aspect_ratio = image.shape[1] / image.shape[0]
desired_height = int(desired_width / aspect_ratio)
resized_image = cv2.resize(image, (desired_width, desired_height))


def onTrackbarChange(value):
    global blk_thresh
    blk_thresh = value
    print("Variable value:", blk_thresh)


def valueScaling(value):
    min_value = 0
    max_value = 100
    new_min = 0
    new_max = 255
    scaled_value = (value - min_value) * (new_max - new_min) / (max_value - min_value) + new_min
    return int(scaled_value)


blk_thresh = 50
scaled_thresh = valueScaling(blk_thresh)

window_name = 'Background Removed'
cv2.namedWindow(window_name)

cv2.createTrackbar('Variable', window_name, scaled_thresh, 100, onTrackbarChange)

while True:
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold_img = cv2.threshold(blur, blk_thresh, 255, cv2.THRESH_BINARY)

    mask = 255 - threshold_img

    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    cv2.imshow(window_name, result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

"""
    Live camera sample showing the camera information and video in real time and allows to control the different
    settings.
"""
"""
import cv2
import pyzed.sl as sl

# Global variable 

camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1
led_on = True
selection_rect = sl.Rect()
select_in_progress = False
origin_rect = (-1, -1)


# Function that handles mouse events when interacting with the OpenCV window.
def on_mouse(event, x, y, flags, param):
    global select_in_progress, selection_rect, origin_rect
    if event == cv2.EVENT_LBUTTONDOWN:
        origin_rect = (x, y)
        select_in_progress = True
    elif event == cv2.EVENT_LBUTTONUP:
        select_in_progress = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        select_in_progress = False
        selection_rect = sl.Rect(0, 0, 0, 0)

    if select_in_progress:
        selection_rect.x = min(x, origin_rect[0])
        selection_rect.y = min(y, origin_rect[1])
        selection_rect.width = abs(x - origin_rect[0]) + 1
        selection_rect.height = abs(y - origin_rect[1]) + 1


def main():
    init = sl.InitParameters()
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : " + repr(status) + ". Exit program.")
        exit()

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    win_name = "Camera Control"
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, on_mouse)
    print_camera_information(cam)
    print_help()
    switch_camera_settings()
    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:  # Check that a new image is successfully acquired
            cam.retrieve_image(mat, sl.VIEW.LEFT)  # Retrieve left image
            cvImage = mat.get_data()  # Convert sl.Mat to cv2.Mat
            if (not selection_rect.is_empty() and selection_rect.is_contained(sl.Rect(0, 0, cvImage.shape[1],
                                                                                      cvImage.shape[
                                                                                          0]))):  # Check if selection rectangle is valid and draw it on the image
                cv2.rectangle(cvImage, (selection_rect.x, selection_rect.y),
                              (selection_rect.width + selection_rect.x, selection_rect.height + selection_rect.y),
                              (220, 180, 20), 2)
            cv2.imshow(win_name, cvImage)  # Display image
        else:
            print("Error during capture : ", err)
            break

        key = cv2.waitKey(5)
        # Change camera settings with keyboard
        update_camera_settings(key, cam, runtime, mat)
    cv2.destroyAllWindows()

    cam.close()


# Display camera information
def print_camera_information(cam):
    cam_info = cam.get_camera_information()
    print("ZED Model                 : {0}".format(cam_info.camera_model))
    print("ZED Serial Number         : {0}".format(cam_info.serial_number))
    print("ZED Camera Firmware       : {0}/{1}".format(cam_info.camera_configuration.firmware_version,
                                                       cam_info.sensors_configuration.firmware_version))
    print("ZED Camera Resolution     : {0}x{1}".format(round(cam_info.camera_configuration.resolution.width, 2),
                                                       cam.get_camera_information().camera_configuration.resolution.height))
    print("ZED Camera FPS            : {0}".format(int(cam_info.camera_configuration.fps)))


# Print help
def print_help():
    print("\n\nCamera controls hotkeys:")
    print("* Increase camera settings value:  '+'")
    print("* Decrease camera settings value:  '-'")
    print("* Toggle camera settings:          's'")
    print("* Toggle camera LED:               'l' (lower L)")
    print("* Reset all parameters:            'r'")
    print("* Reset exposure ROI to full image 'f'")
    print("* Use mouse to select an image area to apply exposure (press 'a')")
    print("* Exit :                           'q'\n")


# update camera setting on key press
def update_camera_settings(key, cam, runtime, mat):
    global led_on
    if key == 115:  # for 's' key
        # Switch camera settings
        switch_camera_settings()
    elif key == 43:  # for '+' key
        # Increase camera settings value.
        current_value = cam.get_camera_settings(camera_settings)[1]
        cam.set_camera_settings(camera_settings, current_value + step_camera_settings)
        print(str_camera_settings + ": " + str(current_value + step_camera_settings))
    elif key == 45:  # for '-' key
        # Decrease camera settings value.
        current_value = cam.get_camera_settings(camera_settings)[1]
        if current_value >= 1:
            cam.set_camera_settings(camera_settings, current_value - step_camera_settings)
            print(str_camera_settings + ": " + str(current_value - step_camera_settings))
    elif key == 114:  # for 'r' key
        # Reset all camera settings to default.
        cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, -1)
        cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, -1)
        print("[Sample] Reset all settings to default")
    elif key == 108:  # for 'l' key
        # Turn on or off camera LED.
        led_on = not led_on
        cam.set_camera_settings(sl.VIDEO_SETTINGS.LED_STATUS, led_on)
    elif key == 97:  # for 'a' key
        # Set exposure region of interest (ROI) on a target area.
        print("[Sample] set AEC_AGC_ROI on target [", selection_rect.x, ",", selection_rect.y, ",",
              selection_rect.width, ",", selection_rect.height, "]")
        cam.set_camera_settings_roi(sl.VIDEO_SETTINGS.AEC_AGC_ROI, selection_rect, sl.SIDE.BOTH)
    elif key == 102:  # for 'f' key
        # Reset exposure ROI to full resolution.
        print("[Sample] reset AEC_AGC_ROI to full res")
        cam.set_camera_settings_roi(sl.VIDEO_SETTINGS.AEC_AGC_ROI, selection_rect, sl.SIDE.BOTH, True)


# Function to switch between different camera settings (brightness, contrast, etc.).
def switch_camera_settings():
    global camera_settings
    global str_camera_settings
    if camera_settings == sl.VIDEO_SETTINGS.BRIGHTNESS:
        camera_settings = sl.VIDEO_SETTINGS.CONTRAST
        str_camera_settings = "Contrast"
        print("[Sample] Switch to camera settings: CONTRAST")
    elif camera_settings == sl.VIDEO_SETTINGS.CONTRAST:
        camera_settings = sl.VIDEO_SETTINGS.HUE
        str_camera_settings = "Hue"
        print("[Sample] Switch to camera settings: HUE")
    elif camera_settings == sl.VIDEO_SETTINGS.HUE:
        camera_settings = sl.VIDEO_SETTINGS.SATURATION
        str_camera_settings = "Saturation"
        print("[Sample] Switch to camera settings: SATURATION")
    elif camera_settings == sl.VIDEO_SETTINGS.SATURATION:
        camera_settings = sl.VIDEO_SETTINGS.SHARPNESS
        str_camera_settings = "Sharpness"
        print("[Sample] Switch to camera settings: Sharpness")
    elif camera_settings == sl.VIDEO_SETTINGS.SHARPNESS:
        camera_settings = sl.VIDEO_SETTINGS.GAIN
        str_camera_settings = "Gain"
        print("[Sample] Switch to camera settings: GAIN")
    elif camera_settings == sl.VIDEO_SETTINGS.GAIN:
        camera_settings = sl.VIDEO_SETTINGS.EXPOSURE
        str_camera_settings = "Exposure"
        print("[Sample] Switch to camera settings: EXPOSURE")
    elif camera_settings == sl.VIDEO_SETTINGS.EXPOSURE:
        camera_settings = sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE
        str_camera_settings = "White Balance"
        print("[Sample] Switch to camera settings: WHITEBALANCE")
    elif camera_settings == sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE:
        camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
        str_camera_settings = "Brightness"
        print("[Sample] Switch to camera settings: BRIGHTNESS")


if __name__ == "__main__":
    main()
    """