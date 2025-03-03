import cv2
import numpy as np
import time
from scipy.signal import butter, filtfilt

# Function to apply a bandpass filter to remove noise
def bandpass_filter(signal, lowcut=0.5, highcut=3.0, fs=30, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Load OpenCV's face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

frame_count = 0
red_values = []
green_values = []

face_detected_time = None  # Track when a face was last seen
last_detected_face = None  # Store the last detected face for a stable ROI

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

    # Check if a face is detected
    if len(faces) > 0:
        face_detected_time = time.time()
        x, y, w, h = faces[0]
        last_detected_face = (x, y, w, h)  # Store last detected face

    # If no face detected for 5 seconds, reset data and stop calculations
    if face_detected_time and (time.time() - face_detected_time > 5):
        print("No face detected for 5 seconds. Pausing SpO2 calculation...")
        red_values = []
        green_values = []
        frame_count = 0  # Reset frame count
        last_detected_face = None

    # Only process SpO₂ if a face is detected
    if last_detected_face:
        x, y, w, h = last_detected_face
        roi_x = max(0, x - int(w * 0.1))
        roi_y = max(0, y - int(h * 0.1))
        roi_w = min(frame.shape[1] - roi_x, int(w * 1.2))
        roi_h = min(frame.shape[0] - roi_y, int(h * 1.2))

        # Convert to RGB and extract ROI
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = rgb_frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Apply Gaussian filter to reduce noise
        roi = cv2.GaussianBlur(roi, (5, 5), 0)

        # Extract mean color intensities
        red_mean = np.mean(roi[:, :, 0])
        green_mean = np.mean(roi[:, :, 1])

        red_values.append(red_mean)
        green_values.append(green_mean)
        frame_count += 1

        # Draw ROI rectangle
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)
        cv2.putText(frame, "Align Your Face Here", (roi_x, roi_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        SpO2 = None

        # Only calculate SpO2 if we have enough data
        if frame_count > 10 and len(red_values) > 33 and len(green_values) > 33:
            red_values_np = np.array(red_values)
            green_values_np = np.array(green_values)

            filtered_red = bandpass_filter(red_values_np, fs=30)
            filtered_green = bandpass_filter(green_values_np, fs=30)

            AC_red = np.std(filtered_red)
            DC_red = np.mean(filtered_red)
            AC_green = np.std(filtered_green)
            DC_green = np.mean(filtered_green)

            R = (AC_red / DC_red) / (AC_green / DC_green)
            SpO2 = 100 - (20 * (R - 0.5))

        if SpO2 is not None:
            cv2.putText(frame, f"Estimated SpO2: {SpO2:.2f}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No Face Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('SpO2 Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("User exited the program.")
        break

cap.release()
cv2.destroyAllWindows()
