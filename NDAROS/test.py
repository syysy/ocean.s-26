import cv2

video = cv2.VideoCapture("video.mp4")

# Move window to second screen (adjust coordinates)
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.moveWindow("Video", 1920, 0)  # If second monitor starts at x=1920

while True:
    ret, frame = video.read()
    if not ret:
        break

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()