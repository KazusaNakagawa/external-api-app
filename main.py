import sys
from src.instagram import Instagram
from src.utils.logger import Logger

_logger = Logger()
logger = _logger.get_logger()


def main():
    """実行コマンド

    Example:
      1. gzip archive
        $ python main.py

      2. obtain data
        $ python main.py -query bluebottle -limit 50
    """
    logger.info("start main")
    if len(sys.argv) == 1:
        _logger.gzip()
    elif len(sys.argv) < 5:
        logger.error("missing argument")
        logger.error("Example: $ python main.py -query bluebottle -limit 50")
    else:
        query: str = sys.argv[2]
        limit: int = int(sys.argv[4])
        instagram = Instagram(
            limit=limit, query=query, business_discovery_username=query
        )
        instagram.run()
    logger.info("end main")


if __name__ == "__main__":
    main()
