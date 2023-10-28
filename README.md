## external-api-app

### Description
Script to retrieve the content of a post via the Instagram Graph API.

### Assumption
1. you have obtained an access token from the [Instagram Platform](https://developers.facebook.com/docs/instagram?locale=en_US)

### Environment
1. Mac M1
2. virtual environment
3. Python 3.9 series


### Usage
1. `.env` file

   ```bash
   cp .env.example .env
   vi .env
   # add your access token and business account id
   ACCESS_TOKEN={this is your access token}
   BUSINESS_ACCOUNT_ID={this is your business account id}
   ```

2. create virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages

   ```bash
   pip install -r requirements.txt
   ```

4. Run the main script

   ```bash
    python main.py -query bluebottle -limit 50
    ```

5. Check the results

   ```bash
   ls ./data/instagram
   ```

    ```bash
    ./data
    └── instagram
        └── response_bluebottle_limit50_20231028211611.csv
        └── response_bluebottle_limit50_20231028211611.json
        └── ...
    ```

## Reference
1. [Instagram Platform](https://developers.facebook.com/docs/instagram?locale=en_US)
2. [Instagram Graph API](https://developers.facebook.com/docs/instagram-api?locale=en_US)
3. [Instagram Graph API Reference](https://developers.facebook.com/docs/instagram-api/reference?locale=en_US)
4. [InstagramAPIの始め方！Instagram Graph APIのセットアップ方法を解説](https://tabiato.co.jp/biz/blog/instagram-graph-api-setup/)
5. [Instagram graph APIのアクセストークンを使ってWordPressサイトへInstagramを埋め込む方法](https://calieto.com/calietoblog/embedding-method-instagram-wordpress/#)
