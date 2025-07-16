import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe drawing utilities and pose model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):

    a = np.array(a)  # First point
    b = np.array(b)  # Mid point (vertex of the angle)
    c = np.array(c)  # End point

    # Calculate radians using arctan2
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    # Convert to degrees and take absolute value
    angle = np.abs(radians * 180.0 / np.pi)

    # Ensure angle is within 0-180 degrees
    if angle > 180.0:
        angle = 360 - angle

    return angle


# --- Counter Variables ---
pushup_count = 0
# lunge_count will now track total lunges (left + right)
lunge_count = 0
# plank_count (originally 'flank') - renamed for clarity
plank_count = 0

# Stage variables for exercise tracking
pushup_stage = None  # "down" or "up"
# Dictionary to track lunge stage for each leg
lunge_stage = {"left": "up", "right": "up"}
# plank_state (originally 'foot_state') - renamed for clarity
plank_state = None  # "up" (standing/straight legs) or "down" (plank position)

# --- Video Capture Setup ---
cap = cv2.VideoCapture(0) # 0 for default webcam
# Set frame width and height for better resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

## Setup MediaPipe Pose instance
# min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for the pose detection to be considered successful.
# min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) for the pose landmarks to be considered tracked successfully.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: # Check if frame was successfully read
            print("Failed to grab frame, exiting...")
            break

        # Recolor image from BGR (OpenCV default) to RGB (MediaPipe required)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # Make image non-writeable to improve performance

        # Process the image to make pose detections
        results = pose.process(image)

        # Recolor image back to BGR for OpenCV display
        image.flags.writeable = True # Make image writeable again
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks if detected
        try:
            landmarks = results.pose_landmarks.landmark

            # --- Get coordinates for key body parts ---
            # Left arm
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            # Left leg
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Right arm
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            # Right leg
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]


            # --- Calculate angles ---
            # Push-up angles (elbows)
            left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            avg_elbow_angle = (left_elbow_angle + right_elbow_angle) / 2

            # Lunge angles (knees) - using hip, knee, ankle
            left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # --- Push-up Counter Logic ---
            # If arms are extended (up position)
            # if avg_elbow_angle > 160:
            #     pushup_stage = "up"
            # # If arms are bent (down position) AND was previously in "up" stage
            # elif avg_elbow_angle < 90 and pushup_stage == "up":
            #     pushup_stage = "down"
            #     pushup_count += 1 # Increment push-up count

            # --- Lunge Counter Logic (Improved) ---
            # Thresholds for lunge angles
            LUNGE_DOWN_THRESHOLD = 100 # Angle when knee is bent in lunge
            LUNGE_UP_THRESHOLD = 160   # Angle when leg is straight (standing)

            # Left Lunge
            if left_knee_angle < LUNGE_DOWN_THRESHOLD and lunge_stage["left"] == "up":
                lunge_stage["left"] = "down"
            elif left_knee_angle > LUNGE_UP_THRESHOLD and lunge_stage["left"] == "down":
                lunge_count += 1
                lunge_stage["left"] = "up"

            # Right Lunge
            if right_knee_angle < LUNGE_DOWN_THRESHOLD and lunge_stage["right"] == "up":
                lunge_stage["right"] = "down"
            elif right_knee_angle > LUNGE_UP_THRESHOLD and lunge_stage["right"] == "down":
                lunge_count += 1
                lunge_stage["right"] = "up"

            # --- Plank Counter Logic (using knee angles, as per original code) ---
            # Note: A more robust plank counter would involve checking hip and shoulder alignment
            # and overall body straightness, not just knee angles.
            # This logic assumes "plank" means bending knees significantly.
            # foot_avg_angle = (left_knee_angle + right_knee_angle) / 2 # Renamed from foot_avg_angle for clarity
            #
            # if foot_avg_angle > 160: # Legs straight (up position for plank)
            #     plank_state = "up"
            # elif foot_avg_angle < 90 and plank_state == "up": # Legs bent (down position for plank)
            #      plank_state = "down"
            #      plank_count += 1 # Increment plank count
            #

            # --- Visualize angles on screen ---
            # Scale landmark coordinates to image resolution for display
            image_width, image_height, _ = image.shape
            scale_x = 1920 # Landmarks are normalized (0-1)
            scale_y = 1080

            # cv2.putText(image, f'L-Elbow: {int(left_elbow_angle)}',
            #             tuple(np.multiply(left_elbow, [scale_x, scale_y]).astype(int)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            #
            # cv2.putText(image, f'R-Elbow: {int(right_elbow_angle)}',
            #             tuple(np.multiply(right_elbow, [scale_x, scale_y]).astype(int)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, f'L-Knee: {int(left_knee_angle)}',
                        tuple(np.multiply(left_knee, [scale_x, scale_y]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, f'R-Knee: {int(right_knee_angle)}',
                        tuple(np.multiply(right_knee, [scale_x, scale_y]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        except Exception as e:
            # Print error if landmark detection fails
            print(f"Error extracting landmarks or calculating angles: {e}")
            pass # Continue to next frame even if detection fails for one frame

        # --- Display Counters and Stages ---
        # Draw a rectangle for the display area
        cv2.rectangle(image, (0, 0), (700, 120), (245, 117, 16), -1) # Increased width for more text

        # Push-up count display
        # cv2.putText(image, 'PUSH-UPS', (15, 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(image, str(pushup_count), (15, 70),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        #
        # # Plank count display
        # cv2.putText(image, 'PLANKS', (200, 30), # Renamed 'flank-UPS' to 'PLANKS'
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(image, str(plank_count), (200, 70),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Lunge count display
        cv2.putText(image, 'LUNGES', (400, 30), # Renamed 'lanunge' to 'LUNGES'
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, str(lunge_count), (400, 70), # Fixed typo '7q0' to '70'
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Stage display (for push-ups)
        # cv2.putText(image, 'STAGE', (580, 30), # Adjusted position
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(image, pushup_stage if pushup_stage else 'None', (580, 80), # Adjusted position
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Render MediaPipe pose detections (landmarks and connections)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Display the image
        cv2.imshow('Exercise Counter', image) # Changed window title

        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
