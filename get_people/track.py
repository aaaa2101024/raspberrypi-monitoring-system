import cv2
from ultralytics import YOLO
import datetime
import csv

CENTRAL = 320
PEOPLE = 0


class Track:
    def __init__(self):
        # 左側からの検出か右側からの検出かを分け, 使用済みidを記録することとする
        self.left = set()
        self.right = set()
        self.used_id = set()
        self.people_count = 0
        # yoloとopencvの変数たち
        # ここの変数はカメラが何かで変える必要がある
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("./get_people/yolo11n.pt")
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def add_csv(self, track_id, tag):
        current_time = datetime.datetime.now()
        time = current_time.strftime(self.time_format)
        date = []
        date.append(track_id)
        date.append(time)
        date.append(tag)
        date.append(self.people_count)
        with open("./data/result.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(date)

    def check_people(self, track_id, x):
        # 登録されていないidであったら登録処理
        if track_id not in self.used_id:
            # 左側か右側かを判定
            self.used_id.add(track_id)
            if x < CENTRAL:
                self.left.add(track_id)
                self.used_id.add(track_id)
            else:
                self.right.add(track_id)
                self.used_id.add(track_id)

        # 人数の増減判定
        # 左側(部屋の人数増加)
        if track_id in self.left and x >= CENTRAL:
            self.people_count += 1
            self.left.discard(track_id)
            self.right.add(track_id)

            # add csv
            self.add_csv(track_id, "in")

        # 右側(部屋の人数減少)
        if track_id in self.right and x < CENTRAL:
            self.people_count -= 1
            self.right.discard(track_id)
            self.left.add(track_id)

            # add csv
            self.add_csv(track_id, "out")

    def show_image(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("映像が取得できませんでした")
                break

            # yoloを動かして検知させる
            # confが閾値, classesが検出する対象
            # persistがIDを保持する設定, verboseがログを出力するかどうか
            results = self.model.track(
                frame,
                imgsz=256,
                conf=0.5,
                classes=[PEOPLE],
                persist=True,
                verbose=False,
            )

            # 結果をフレームに描画して表示
            annotated_frame = results[0].plot()

            # 値の取得などを行うなど
            items = results[0]
            for item in items:  # 1つ取得

                # バウンディングボックスの座標を取得
                # xがx座標の中心
                x, y, w, h = item.boxes.xywh.cpu().numpy()[0]
                id_value = item.boxes.id  # トラッキングIDを取得 存在しない場合はNone
                if id_value is None:  # トラッキングIDが存在しないなら空文字
                    track_id = ""
                else:  # 存在すればIDを取得
                    track_id = item.boxes.id.int().cpu().tolist()[0]

                # 部屋の人数カウントの検証を行う
                if not track_id == "":
                    self.check_people(track_id, x)

            # # リサイズ
            # # yoloを適用する過程で、4 : 3になるのに留意
            # annotated_frame = cv2.resize(annotated_frame, (1000, 750))

            # 映像を垂れ流す
            # cv2.imshow("camera", annotated_frame)

            # 部屋人数の出力
            print("people : " + str(self.people_count))

            # 'q'を押すと終了
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.cap.release()
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    track = Track()
    track.show_image()
