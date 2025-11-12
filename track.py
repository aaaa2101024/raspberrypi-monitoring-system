import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(1)
model = YOLO("yolo11n.pt")

def show_image():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("映像が取得できませんでした")
            break

        # ここでyoloを動かして検知させる
        results = model.track(frame, conf=0.5)

        # 結果をフレームに描画して表示
        annotated_frame = results[0].plot()

        # 値の取得などを行うなど
        # リサイズ
        # yoloを適用する過程で、4 : 3になるのに留意
        annotated_frame = cv2.resize(annotated_frame, (1000, 750))

        # 映像を垂れ流す
        cv2.imshow("camera", annotated_frame)

        # 'q'を押すと終了
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    show_image()
