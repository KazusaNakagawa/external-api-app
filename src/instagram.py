import json
import os
import sys
import time
import requests
from dotenv import load_dotenv

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.utils.logger import Logger

_logger = Logger(__file__.split("/")[-1].replace(".py", ""))
logger = _logger.get_logger()

load_dotenv()
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
BUSINESS_ACCOUNT_ID = os.environ.get("BUSINESS_ACCOUNT_ID")


_DATA_DIR = "data/instagram"
_DATE_FORMAT = time.strftime("%Y%m%d%H%M%S")


class InstagramAPI:
    def __init__(
        self,
        limit: int = 50,
        query: str = "bluebottle",
        business_discovery_username: str = "bluebottle",
    ):
        self.limit = limit
        self.query = query
        self.business_discovery_username = business_discovery_username

    def search_ig_hashtag_id(self):
        """Request to the Instagram Graph API.
        - ig_hashtag_id
        """
        url = (
            f"https://graph.facebook.com/v18.0/ig_hashtag_search?"
            + f"user_id={BUSINESS_ACCOUNT_ID}"
            + f"&q={self.query}"
            + f"&access_token={ACCESS_TOKEN}"
        )
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        logger.info(response.status_code)
        res = response.json()
        res = {
            "query": self.query,
            "id": res["data"][0]["id"],
        }
        logger.info(res)
        return res

    def search_recent_media(self, ig_hash_tag_id: str):
        """Request to the Instagram Graph API.
        - recent_media
        """
        url = (
            "https://graph.facebook.com/v18.0/"
            + f"{ig_hash_tag_id}/recent_media"
            + f"?fields=id%2Cmedia_type%2Ccomments_count%2Clike_count%2Ccaption%2Ctimestamp%2Cmedia_url%2Cpermalink"
            + "%2Cchildren{id%2Ctimestamp%2Cmedia_url}"
            + f"&limit={self.limit}"
            + "&transport=cors"
            + f"&user_id={BUSINESS_ACCOUNT_ID}&access_token={ACCESS_TOKEN}"
        )

        headers = {
            "Content-Type": "application/json",
        }
        # リクエスト
        response = requests.get(url, headers=headers)
        logger.info({"response code": response.status_code})
        res = response.json()

        if response.status_code == 200:
            return res
        else:
            logger.error({"msg": res["error"]["message"].split("access_token=")[0]})
            return False

    def search_business_discovery(self):
        """Request to the Instagram Graph API.
        - business_discovery
        """
        url = (
            "https://graph.facebook.com/v18.0/"
            + f"{BUSINESS_ACCOUNT_ID}"
            + f"?fields=business_discovery.username({self.business_discovery_username})"
            + f"%7Bmedia.limit({self.limit})%7Bid%2Cusername%2Ccaption%2Ccomments_count%2Clike_count%2Cmedia_product_type%2Cmedia_url%2Cpermalink%2Ctimestamp%7D%7D"
            + f"&access_token={ACCESS_TOKEN}"
        )
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        logger.info({"response code": response.status_code})

        res = response.json()
        if response.status_code == 200:
            logger.debug(res)
            # data key で取得
            return res["business_discovery"]["media"]
        else:
            logger.error({"msg": res["error"]["message"].split("access_token=")[0]})
            return False

    def count(self, res: dict):
        """Count the number of posts."""
        # 投稿数をカウントする
        if not res:
            logger.info("投稿がありません")
            return False
        count = len(res["data"])
        logger.info(f"投稿数: {count}")
        return True

    def get_media_url(self, res: dict):
        """Get media_url."""
        # media_url を取得する
        for article in res["data"]:
            logger.info(article["media_url"])

    def get_caption(self, res: dict):
        """Get caption."""
        # caption を取得する
        for article in res["data"]:
            logger.info(article["caption"])

    def save_json(self, key_name, res: dict):
        """Save json file."""

        # ディレクトリがなければ作成する
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)

        with open(
            f"{_DATA_DIR}/response_{key_name}_limit{self.limit}_{_DATE_FORMAT}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(res, f, indent=4)

    def read_json(self, key_name):
        """Read json file."""
        with open(
            f"{_DATA_DIR}/response_{key_name}_limit{self.limit}_{_DATE_FORMAT}.json",
            "r",
        ) as f:
            res = json.load(f)

        return res

    def save_csv(self, key_name, res: dict):
        """Save csv file."""
        with open(
            f"{_DATA_DIR}/response_{key_name}_limit{self.limit}_{_DATE_FORMAT}.csv",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                "id,media_type,comments_count,like_count,caption,timestamp,media_url,permalink\n"
            )
            for article in res["data"]:
                f.write(f"{article['id']},")
                f.write(f"{article['media_type']}," if "media_type" in article else ",")
                f.write(f"{article['comments_count']},")
                if "like_count" not in article:
                    article["like_count"] = 0
                f.write(f"{article['like_count']},")
                if "caption" not in article:
                    article["caption"] = ","
                f.write(
                    f"{article['caption']}".replace("\n", "")
                    .replace("\r", "")
                    .replace("\u2615", "")
                    .replace(",", "")
                )
                # caption 格納後に「,」を追加. replace で削除しているため
                f.write(",")
                f.write(f"{article['timestamp']},")
                # media_ur1 はある場合のみ
                f.write(f"{article['media_url']}," if "media_url" in article else ",")
                f.write(f"{article['permalink']}\n")

    def get_recent_media(self, res: dict):
        """Get recent media."""
        res = self.search_recent_media(ig_hash_tag_id=res["id"])
        self.save_json(key_name=self.query, res=res)
        # レスポンスを読み込む
        res = self.read_json(key_name=self.query)
        # 投稿数をカウントする
        if self.count(res):
            self.save_csv(key_name=self.query, res=res)

    def get_business_discovery(self):
        """Get business discovery."""
        key_name = self.business_discovery_username + "_business"
        res = self.search_business_discovery()
        self.save_json(key_name=key_name, res=res)
        # レスポンスを読み込む
        res = self.read_json(key_name=key_name)
        # 投稿数をカウントする
        if self.count(res):
            self.save_csv(key_name=key_name, res=res)

    def run(self):
        """API: 20回 5%

        単純に, 100% には、 20 * 20 = 400 回のリクエストで上限に達する.
        一定期間: 何分か
        200 call 80%
        5%: 20 call
        100%: 400 call

        上限:
        レート制限は40分後に解除されます。
        """
        # ig_hashtag_id を取得する
        res = self.search_ig_hashtag_id()
        self.get_recent_media(res)

        # business_discovery を取得する
        self.get_business_discovery()
