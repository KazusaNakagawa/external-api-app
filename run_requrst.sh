# 以下のようにすると、-query に指定したキーワードを変数に入れて、
# それを使ってコマンドを実行できる
# また、-limit に指定した数だけ、ループで回す
# Usage: bash run_request.sh

for keyword in bluebook 花火 お祭り たこやき
  do
      docker-compose exec app python main.py -query $keyword -limit 50
  done
