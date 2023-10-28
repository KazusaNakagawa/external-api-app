import glob
import gzip
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, name: str):
        self.name = name

    def get_logger(self, log_dir="./logs"):
        """Get logger."""
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s(%(lineno)d) - %(message)s"
        )

        handler = TimedRotatingFileHandler(
            filename=f"{log_dir}/{self.name}.log",
            when="D",
            interval=1,
            backupCount=7,
            encoding="utf-8",
            delay=False,
            utc=True,
        )
        handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(stream_handler)

        return logger

    def remove(self, log_dir="./logs", max_file_num=3) -> None:
        """指定ファイル以上ある場合は古いファイルを削除. 更新日時でソート

        Args:
            log_dir (str, optional): [description]. Defaults to './logs'.
            max_file_num (int, optional): [description]. Defaults to 3.

        """
        if len(glob.glob(f"{log_dir}/*")) > max_file_num:
            files = sorted(glob.glob(f"{log_dir}/*"), key=os.path.getmtime)
            os.remove(files[0])

    def gzip(self, log_dir="./logs") -> None:
        """All Compress log file.

        Args:
            log_dir (str, optional): [description]. Defaults to './logs'.

        """
        for file in glob.glob(f"{log_dir}/*"):
            if file.endswith(".gz"):
                continue
            # 日付のフォーマットを変更
            result = re.search(r"\d{4}-\d{2}-\d{2}", file)
            if result:
                rep_ = result.string.replace("-", "").replace("_", "")
                os.rename(file, rep_)
                file = rep_

            with open(file, "rb") as f_in:
                with gzip.open(f"{file}.gz", "wb") as f_out:
                    f_out.writelines(f_in)
            os.remove(file)

    def log_rotation(self):
        """ログローテーション"""
        self.gzip()
        self.remove()
