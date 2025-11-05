import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
model = YOLO("yolo11m.pt")


def show_image():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("映像が取得できませんでした")
            break

        # JPEGに圧縮
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        result, encimg = cv2.imencode(".jpg", frame, encode_param)
        data = encimg.tobytes()

        # ここでyoloを動かして検知させる
        results = model(frame)

        # 結果をフレームに描画して表示
        annotated_frame = results[0].plot()

        # 映像を垂れ流す
        cv2.imshow("camera", annotated_frame)

        # 'q'を押すと終了
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    show_image()
