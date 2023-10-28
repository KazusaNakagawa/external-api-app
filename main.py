import sys
from src.instagram import InstagramAPI
from src.utils.logger import Logger

_logger = Logger(__file__.split("/")[-1].replace(".py", ""))
logger = _logger.get_logger()

DATA_DIR = "data/instagram"


def main():
    """実行コマンド

    Example:
      1. gzip archive
        $ python main.py

      2. obtain data
        $ python main.py -query bluebottle -limit 50
    """
    if len(sys.argv) == 1:
        _logger.gzip(DATA_DIR)
    elif len(sys.argv) < 5:
        logger.error("missing argument")
        logger.error("Example: $ python main.py -query bluebottle -limit 50")
        sys.exit()
    else:
        query: str = sys.argv[2]
        limit: int = int(sys.argv[4])
        instagram = InstagramAPI(limit=limit, query=query)
        instagram.run()


if __name__ == "__main__":
    main()
