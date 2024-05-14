from flask import Flask, render_template, Response, send_file
import cv2

app = Flask(__name__)

ip="라즈베리파이 고유의 ip"
video_file = "영상 파일 경로"

def gen_frames():
    capture = cv2.VideoCapture(0)  # 카메라 캡처 초기화.
    while True:
        ref, frame = capture.read()  # 현재 영상을 받아옴.
        if not ref:  # 영상이 잘 받아지지 않았으면 무한 루프 종료.
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 이미지 프레임 반환.

@app.route('/')#사용자가 보기위함.
def index():
    return "<html><body><img src='/video_feed' /></body></html>"
#http://<라즈베리파이의 IP 주소>:5000로 접속하면 카메라를 볼 수 있음.

@app.route('/download_video') # 영상 다운로드.
def download_video():
    return send_file(video_file, as_attachment=True)

@app.route('/video_feed')#카메라의 크기.
def video_feed():
   return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
   app.run(host=ip, port=5000)
