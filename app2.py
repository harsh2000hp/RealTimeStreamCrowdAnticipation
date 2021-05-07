from flask import Flask, render_template, Response
import cv2
from gaze_tracking import GazeTracking
import datetime
app = Flask(__name__)
gaze = GazeTracking()
camera = cv2.VideoCapture(0)# use 0 for web camera
attentionPercentage = 0


#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    centerFrames = 1
    leftFrames = 0
    rightFrames = 0
    noVisionFrames = 0
    sleepingFrames = 0

    while True:

        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break


        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        text = "Initial Text"
        if gaze.is_blinking():
            text = "Kindly Blinking"
            sleepingFrames=sleepingFrames+1

        elif gaze.is_right():
            text = "Looking Right"
            rightFrames=rightFrames+1



        elif gaze.is_left():
            text = "Looking Left"
            leftFrames=leftFrames+1


        elif gaze.is_center():
            text = "Looking Center"
            centerFrames=centerFrames+1

        else:
            text = "No Vision Found"
            noVisionFrames=noVisionFrames+1





        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        attentionPercentage= float(100*centerFrames/(centerFrames+leftFrames+rightFrames+sleepingFrames+noVisionFrames))

        outAttentionPercentage = open("outAttentionPercentage.txt", "w")
        outAttentionPercentage.write("AttentionPercentage: " + str(attentionPercentage))

        outCentralFrames = open('outCentralFrames.txt','w')
        outCentralFrames.write("Central Frames: " + str(centerFrames))

        outRightFrames = open('outRightFrames.txt', 'w')
        outRightFrames.write("Right Frames: " + str(rightFrames))

        outLeftFrames = open('outLeftFrames.txt', 'w')
        outLeftFrames.write("Left Frames: " + str(leftFrames))

        outSleepingFrames = open('outSleepingFrames.txt', 'w')
        outSleepingFrames.write("Sleeping Frames: " + str(sleepingFrames))

        outNoVisionFrames = open('outNoVisionFrames.txt', 'w')
        outNoVisionFrames.write("No Vision Frames: " + str(noVisionFrames))





        yield ((b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'))











@app.route('/video_feed')
def video_feed():


    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/button')
def AttentionValueReturn():
    File1 = open('outAttentionPercentage.txt', 'r')
    File2 = open('outLeftFrames.txt','r')
    File3 = open('outRightFrames.txt','r')
    File4 = open('outCentralFrames.txt','r')
    File5 = open('outSleepingFrames.txt','r')
    File6 = open('outNoVisionFrames.txt','r')



    return render_template('button.html',valueFinale1 = File1.read(),valueFinale2 = File2.read(),valueFinale3 = File3.read(),valueFinale4 = File4.read(),valueFinale5 = File5.read(),valueFinale6 = File6.read())


if __name__ == '__main__':
    app.run(debug=True)

#
#
# for value in gen_frames():
#     print(value)
#     if value == 'No Vision Found':
#         noVisionFrames = noVisionFrames+1
#     if value == 'Kindly Blinking':
#         sleepingFrames = sleepingFrames+1
#     if value == 'Looking Right':
#         rightFrames = rightFrames+1
#     if value == 'Looking Left':
#         leftFrames = leftFrames+1
#     if value == 'Looking Center':
#         centerFrames = centerFrames+1
#
#     attentionPercentage = float (100*centerFrames/(centerFrames+leftFrames+rightFrames+noVisionFrames+sleepingFrames))
#     print(attentionPercentage)


