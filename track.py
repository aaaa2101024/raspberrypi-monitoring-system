import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(1)
model = YOLO("yolo11n.pt")

CENTRAL = 320
PEOPLE = 0

# 左側からの検出か右側からの検出かを分け, 使用済みidを記録することとする
left = set()
right = set()
used_id = set()

def show_image():
    people_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("映像が取得できませんでした")
            break

        # yoloを動かして検知させる
        results = model.track(frame, conf=0.5, persist=True, verbose=False)

        # 結果をフレームに描画して表示
        annotated_frame = results[0].plot()

        # 値の取得などを行うなど
        items = results[0]
        for item in items:  # 1つ取得
            # peopleなら0が返ってくる
            cls = int(item.boxes.cls)  # クラスIDを取得

            x, y, w, h = item.boxes.xywh.cpu().numpy()[
                0
            ]  # バウンディングボックスの座標を取得

            id_value = item.boxes.id  # トラッキングIDを取得 存在しない場合はNone
            if id_value is None:  # トラッキングIDが存在しないなら空文字
                track_id = ""
            else:  # 存在すればIDを取得
                track_id = item.boxes.id.int().cpu().tolist()[0]

            # 人間検出の場合, 部屋の人数カウントの検証を行う
            if cls == PEOPLE:
                # 登録されていないidであったら登録処理
                if track_id not in used_id:
                    # 左側か右側かを判定
                    used_id.add(track_id)
                    if x < CENTRAL:
                        left.add(track_id)
                    else:
                        right.add(track_id)

                # 人数の増減判定
                # 左側(部屋の人数増加)
                if track_id in left and x >= CENTRAL:
                    people_count += 1
                    left.discard(track_id)
                # 右側(部屋の人数減少)
                if track_id in right and x < CENTRAL:
                    people_count -= 1
                    right.discard(track_id)

        # リサイズ
        # yoloを適用する過程で、4 : 3になるのに留意
        annotated_frame = cv2.resize(annotated_frame, (1000, 750))

        # 映像を垂れ流す
        cv2.imshow("camera", annotated_frame)

        # 部屋人数の出力
        print("people : " + str(people_count))

        # 'q'を押すと終了
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    show_image()
