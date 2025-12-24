# 先端技術演習用
テスト

install ambient
```python
pip install git+https://github.com/AmbientDataInc/ambient-python-lib.git
```

program start
```
cd ./sentan
python -m send_data.send_data
python -m send_infrared
python -m get_people.track
```

# 備忘録
## codes.jsonの位置について
./sentanでプログラムを起動する関係上, ./sentan直下に置けば大丈夫\
他に置くと怒られる