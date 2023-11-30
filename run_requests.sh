# 以下のようにすると、-query に指定したキーワードを変数に入れて実行できる
# Usage: ./run_requests.sh

for keyword in bluebook 花火 お祭り たこやき
  do
      docker-compose exec app python main.py -query $keyword -limit 50
  done
