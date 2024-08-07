import numpy as np
import cv2
import logs

global tracking, old_points, init_point, lk_params

# Mouse callback function
def select_point(event, x, y, flags, param):
    global tracking, init_point, old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        init_point = (x, y)
        old_points = np.array([[x, y]], dtype=np.float32).reshape(-1, 1, 2)
        tracking = True


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
    global tracking, old_points, init_point, lk_params


    # Initialize variables for tracking
    tracking = False
    init_point = None
    old_points = None
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, -64)

    # Window
    combined_window_name = "track point and detect green light"
    cv2.namedWindow(combined_window_name, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(combined_window_name, select_point)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    comments = []
    timestamp = 0.0

    while True:
        cap.set(cv2.CAP_PROP_BRIGHTNESS, -64)
        ret, frame = cap.read()
        if frame is None:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        image = frame.copy()
        red = image[:, :, 2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([45, 100, 100])
        upper_green = np.array([75, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_loc = get_center_of_mask(green_mask)
        if green_loc is not None:
            command = "drone_point", "x:", green_loc[0], "y:", green_loc[1]
            timestamp += 0.02  # Increment timestamp (adjust as necessary)
            comments.append(f"Time: {timestamp:.2f} seconds - Command: {command}")
            print("drone_point", green_loc)

        # if green_loc is not None:
        #     cv2.circle(image, green_loc, 5, (0, 255, 0), 2)

        #(minVal, maxVal, minLoc, maxLoc_red) = cv2.minMaxLoc(red)
        #cv2.circle(image, maxLoc_red, 5, (0, 0, 255), 2)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if tracking:
            new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, old_points, None, **lk_params)
            for i, (new, old) in enumerate(zip(new_points, old_points)):
                a, b = new.ravel()
                c, d = old.ravel()
                #image = cv2.circle(image, (int(a), int(b)), 5, (225, 0, 0), -1)

                # target_point = (int(a), int(b))
                # comment = logs.create_commands("target_point", int(a),  int(b))
                # logs.save_commands_to_log(comment)
                #
                # print("target_point", target_point)

            old_gray = frame_gray.copy()
            old_points = new_points.reshape(-1, 1, 2)



        cv2.imshow(combined_window_name, image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logs.save_commands_to_log(comments)

if __name__ == '__main__':
    main()
