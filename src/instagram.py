import json
import os
import sys
import time
import requests
from dotenv import load_dotenv

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.utils.db import Database
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
        """Instagram API.
        - ig_hashtag_id
        - recent_media
        - business_discovery

        Args:
            limit (int, optional): [description]. Defaults to 50.
            query (str, optional): [description]. Defaults to "bluebottle".
            business_discovery_username (str, optional): [description]. Defaults to "bluebottle".

            Examples:
                >>> from src.instagram import InstagramAPI
                >>> instagram = InstagramAPI(limit=50, query="bluebottle", business_discovery_username="bluebottle")
                >>> instagram.run()
        """
        self.limit = limit
        self.query = query
        self.business_discovery_username = business_discovery_username

    def search_ig_hashtag_id(self) -> dict:
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
        res = response.json()

        if response.status_code == 200:
            res = {
                "query": self.query,
                "id": res["data"][0]["id"],
            }
            logger.info(res)
            return res
        else:
            logger.error({"msg": res})
            return {}

    def search_recent_media(self, ig_hash_tag_id: str) -> dict:
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
            logger.error({"msg": res})
            return {}

    def search_business_discovery(self) -> dict:
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
            logger.error({"msg": res})
            return {}


class Instagram(InstagramAPI):

    """Instagram API.
    - ig_hashtag_id
    - recent_media
    - business_discovery

    Args:
        InstagramAPI ([type]): [description]
    """

    def __init__(
        self,
        limit: int = 50,
        query: str = "bluebottle",
        business_discovery_username: str = "bluebottle",
    ):
        super().__init__(
            limit=limit,
            query=query,
            business_discovery_username=business_discovery_username,
        )

    def save_json(self, key_name, res: dict) -> None:
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

    def save_csv(self, key_name, res: dict) -> None:
        """Save csv file."""
        csv_file = (
            f"{_DATA_DIR}/response_{key_name}_limit{self.limit}_{_DATE_FORMAT}.csv"
        )
        logger.info({"save file": csv_file})
        with open(
            csv_file,
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
        logger.info({"save done": csv_file})

    def count(self, res: dict) -> bool:
        """Count the number of posts."""
        # 投稿数をカウントする
        if not res:
            logger.info("投稿がありません")
            return False
        count = len(res["data"])
        logger.info(f"投稿数: {count}")
        return True

    def get_recent_media(self, res: dict) -> None:
        """Get recent media."""
        if not res:
            logger.info("Not ig_hashtag_id")
            return None

        res = self.search_recent_media(ig_hash_tag_id=res["id"])
        self.save_json(key_name=self.query, res=res)
        res = self.read_json(key_name=self.query)
        # 投稿数をカウントする
        if self.count(res):
            self.save_csv(key_name=self.query, res=res)

    def get_hashtag_media(self) -> None:
        """Get hashtag media."""

        try:
            db = Database("instagram.db")
            ig_hashtag_id = db.select_ig_hashtag_id(name=self.query)
            if ig_hashtag_id:
                logger.info("ig_hashtag_id is already exists")
                self.get_recent_media(res={"id": ig_hashtag_id})
            else:
                res = self.search_ig_hashtag_id()
                db.insert_ig_hashtag_id(name=res["query"], ig_hashtag_id=res["id"])
                self.get_recent_media(res)
        except Exception as e:
            logger.error(e)
            logger.error("Instagram API Error")
        finally:
            db.close()

    def get_business_discovery(self) -> None:
        """Get business discovery."""
        key_name = self.business_discovery_username + "_business"
        res = self.search_business_discovery()

        if not res:
            logger.info("Not business_discovery")
            return None

        self.save_json(key_name=key_name, res=res)
        res = self.read_json(key_name=key_name)
        # 投稿数をカウントする
        if self.count(res):
            self.save_csv(key_name=key_name, res=res)

    def run(self) -> None:
        """API: 20回 5%

        単純に, 100% には、 20 * 20 = 400 回のリクエストで上限に達する.
        一定期間: 何分か
        200 call 80%
        5%: 20 call
        100%: 400 call

        上限:
        レート制限は40分後に解除されます。
        """
        try:
            # ig_hashtag_id でハッシュタグ投稿を取得する
            self.get_hashtag_media()

            # business_discovery を取得する
            self.get_business_discovery()
        except Exception as e:
            logger.error(e)
            logger.error("Instagram API Error")
