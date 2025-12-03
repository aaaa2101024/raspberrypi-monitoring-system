# 修正箇所：ambientモジュールからAmbientクラスをインポート
import ambient
import pandas as pd
import time
import random
# from ..test.sensor import get_sensor_data
from sensor import get_sensor_data


def get_date():
    out = pd.read_csv("./../data/result.csv")
    return out.tail(1).values.tolist()

CHANNEL_ID = 96959  # チャンネルID
WRITE_KEY = "60a58a651c5cdb19"  # ライトキー

am = ambient(CHANNEL_ID, WRITE_KEY)

print("データ送信を開始します (Ctrl+C で停止)")

try:
    while True:
        # ダミーデータ生成
        temp,humid = get_sensor_data()
        people = get_date()
        print(people[0][3])

        # データ送信 (am.send(...) の部分は変更なし)
        r = am.send({"d1": temp, "d2": humid, "d3":people[0][3]})

        if r.status_code == 200:
            print(f"送信成功: 温度={temp:.2f}, 湿度={humid:.2f}")
        else:
            print(f"送信失敗: {r.status_code}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n停止しました")
