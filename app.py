
from flask import Flask, render_template, Response
import cv2
from gaze_tracking import GazeTracking
import datetime
current_duration = datetime.datetime.now()
next_sec = current_duration + datetime.timedelta(0,1)
change_time = next_sec-current_duration
i=0

app = Flask(__name__)
gaze = GazeTracking()
camera = cv2.VideoCapture(0)


# use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():

    while True:




        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Kindly consider taking a break"

        elif gaze.is_right():
            text = "Looking right"


        elif gaze.is_left():
            text = "Looking left"

        elif gaze.is_center():
            text = "Looking center"



        else:
            text = "No Vision found"






        cv2.putText(frame,"unk", (290, 550), cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 255), 2)
        cv2.putText(frame, "unk", (240, 600), cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 255), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("The Crowd Anticipation Algorithm", frame)

        if cv2.waitKey(1) == 27:
            break

"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

@app.route('/video_feed')
def video_feed():
    center=0
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), )

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)