import numpy as np
import cv2

# Initialize variables for tracking
tracking = False
init_point = None
old_points = None
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Mouse callback function
def select_point(event, x, y, flags, param):
    global tracking, init_point, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        init_point = (x, y)
        old_points = np.array([[x, y]], dtype=np.float32).reshape(-1, 1, 2)
        tracking = True

# Mouse callback for other purposes
mouse_position = [0, 0]
def mouse_callback(event, x, y, flags, param):
    global mouse_position
    if event == 1:
        mouse_position[0] = x
        mouse_position[1] = y

# Video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BRIGHTNESS, -64)

# Windows
window_name = "OpenCV"
cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(window_name, mouse_callback)  # Mouse callback
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)
cv2.namedWindow("red_mask", cv2.WINDOW_AUTOSIZE)

# Trackbar callback functions
def on_saturation_trackbar(val):
    global red_saturation
    red_saturation = val

def on_value_trackbar(val):
    global red_value
    red_value = val

def on_hue_up_trackbar(val):
    global red_hue_up
    red_hue_up = val

def on_hue_low_trackbar(val):
    global red_hue_low
    red_hue_low = val

def get_center_of_mask(mask: np.ndarray):
    kernel = np.ones((10, 10), np.uint8)
    dilate = cv2.dilate(mask, kernel)
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    mass_x, mass_y = np.where(dilate >= 255)
    cent_x = np.average(mass_x)
    cent_y = np.average(mass_y)
    if cent_x >= 0 and cent_y >= 0:
        return round(cent_y), round(cent_x)
    return None

def main():
    global red_saturation, red_value, red_hue_up, red_hue_low, tracking, old_points
    red_saturation = 0
    red_value = 0
    red_hue_up = 0
    red_hue_low = 179

    cv2.createTrackbar("Red Saturation", "red_mask", 0, 255, on_saturation_trackbar)
    cv2.createTrackbar("Red Value", "red_mask", 0, 255, on_value_trackbar)
    cv2.createTrackbar("Red Hue up", "red_mask", 0, 179, on_hue_up_trackbar)
    cv2.createTrackbar("Red Hue low", "red_mask", 179, 179, on_hue_low_trackbar)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    while True:
        cap.set(cv2.CAP_PROP_BRIGHTNESS, -64)
        ret, frame = cap.read()
        if frame is None:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        image = frame.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        red = image[:, :, 2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([45, 100, 100])
        upper_green = np.array([75, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_loc = get_center_of_mask(green_mask)

        if green_loc is not None:
            cv2.circle(image, green_loc, 5, (0, 255, 0), 2)

        cv2.imshow('green_mask', green_mask)

        (minVal, maxVal, minLoc, maxLoc_red) = cv2.minMaxLoc(red)
        cv2.circle(image, maxLoc_red, 5, (0, 0, 255), 2)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if tracking:
            new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, old_points, None, **lk_params)
            for i, (new, old) in enumerate(zip(new_points, old_points)):
                a, b = new.ravel()
                c, d = old.ravel()
                frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
            old_gray = frame_gray.copy()
            old_points = new_points.reshape(-1, 1, 2)

        cv2.imshow('Frame', frame)
        cv2.imshow(window_name, image)

        mouse_x, mouse_y = mouse_position
        print(F"mouse_hsv: {hsv[mouse_y, mouse_x]}, red: {maxLoc_red}, green: {green_loc}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
