# 修正箇所：ambientモジュールからAmbientクラスをインポート
from ambient import Ambient
import pandas as pd
import time

# from ..test.sensor import get_sensor_data
from sensor.sensor import get_sensor_data
from data.get_data import get_people_count

CHANNEL_ID = 96959  # チャンネルID
WRITE_KEY = "60a58a651c5cdb19"  # ライトキー

am = Ambient(CHANNEL_ID, WRITE_KEY)

print("データ送信を開始します (Ctrl+C で停止)")

try:
    while True:
        # ダミーデータ生成
        temp, humid = get_sensor_data()
        people = get_people_count()
        print(people)

        # データ送信 (am.send(...) の部分は変更なし)
        r = am.send({"d1": temp, "d2": humid, "d3": people})

        if r.status_code == 200:
            print(f"送信成功: 温度={temp:.2f}, 湿度={humid:.2f}")
        else:
            print(f"送信失敗: {r.status_code}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n停止しました")
