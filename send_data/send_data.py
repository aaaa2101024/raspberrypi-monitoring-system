# 修正箇所：ambientモジュールからAmbientクラスをインポート
from ambient import Ambient
import time

# from ..test.sensor import get_sensor_data
from sensor.sensor import get_sensor_data
from data.get_data import get_people_count
from send_infrared.send_infrared import Send_infrared

# 環境変数
from setting import CHANNEL_ID
from setting import WRITE_KEY

class Send_data:
    def __init__(self):
        self.am = Ambient(CHANNEL_ID, WRITE_KEY)
        self.send_infrared = Send_infrared()
        self.SLEEP_TIME = 10
    
    def main(self):
        print("データ送信を開始します (Ctrl+C で停止)")
        try:
            while True:
                # ダミーデータ生成
                temp, humid = get_sensor_data()
                people = get_people_count()
                print(people)
                # cpntrol airconditonor and get flag
                airconditonor_flag = self.send_infrared.control_airconditioner(people)

                # データ送信 (am.send(...) の部分は変更なし)
                r = self.am.send({"d1": temp, "d2": humid, "d3": people, "d4": airconditonor_flag})

                if r.status_code == 200:
                    print(f"送信成功: 温度={temp:.2f}, 湿度={humid:.2f}")
                else:
                    print(f"送信失敗: {r.status_code}")
                time.sleep(self.SLEEP_TIME)
        except KeyboardInterrupt:print("\n停止しました")


if __name__ == "__main__":
    send_data = Send_data()
    send_data.main()