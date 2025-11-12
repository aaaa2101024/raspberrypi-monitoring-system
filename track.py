import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(1)
model = YOLO("yolo11n.pt")

# 検出開始位置を記録する配列
# 未検出を-1とする
first_detection = [-1] * 100

def show_image():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("映像が取得できませんでした")
            break

        # yoloを動かして検知させる
        results = model.track(frame, conf=0.5)

        # 結果をフレームに描画して表示
        annotated_frame = results[0].plot()

        # 値の取得などを行うなど
        items = results[0]
        for item in items:  # 1つ取得
            # peopleなら0が返ってくる
            cls = int(item.boxes.cls)  # クラスIDを取得

            x, y, w, h = item.boxes.xywh.cpu().numpy()[0]  # バウンディングボックスの座標を取得

            id_value = item.boxes.id  # トラッキングIDを取得 存在しない場合はNone
            if id_value is None:  # トラッキングIDが存在しないなら空文字
                track_ids = ""
            else:  # 存在すればIDを取得
                track_ids = item.boxes.id.int().cpu().tolist()[0]
            
            # 検出対象が人で初めて検出する対象ならば初期位置を記録する
            if first_detection == -1:
                pass
        
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
