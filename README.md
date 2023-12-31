## external-api-app

### Description

Script to retrieve the content of a post via the Instagram Graph API.

### Assumption

1. you have obtained an access token from the [Instagram Platform](https://developers.facebook.com/docs/instagram?locale=en_US)

### Usage (Docker)

**Execution Procedure**

1. `.env` file

   ```bash
   cp .env.example .env
   vi .env
   # add your access token and business account id
   ACCESS_TOKEN={this is your access token}
   BUSINESS_ACCOUNT_ID={this is your business account id}
   ```

2. Build the image

   ```bash
   docker-compose up -d --build
   ```

3. Run the main script

   ```bash
   docker-compose exec app python main.py -query bluebottle -limit 50
   ```

### Usage (virtual environment)

**Environment**

1. Mac M1
2. virtual environment
3. Python 3.9 series

**Execution Procedure**

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

## Document
1. [Instagram Graph API で投稿データを取得する](https://zenn.dev/kazusa_nakagawa/articles/article10_instagram_api)


## Flow Chart

### Main

   ```mermaid
   graph TB
      Start(Start) --> CheckArgs{Check command line arguments}
      CheckArgs -->|One argument| Gzip
      CheckArgs -->|Less than 5 arguments| MissingArg(Missing argument error)
      CheckArgs -->|5 or more arguments| RunInstagram
      Gzip --> End(End)
      MissingArg --> End
      RunInstagram --> End
   ````

### InstagramAPI Class

   ```mermaid
   graph TB
      A[InstagramAPI クラスの初期化] -->|search_ig_hashtag_id| B[Instagram Graph API にリクエスト]
      B --> C[レスポンスの確認]
      C -->|ステータスコードが200| D[レスポンスのログ出力と返却]
      C -->|それ以外| E[エラーログの出力と空の辞書の返却]
      A -->|search_recent_media| F[Instagram Graph API にリクエスト]
      F --> G[レスポンスの確認]
      G -->|ステータスコードが200| H[レスポンスの返却]
      G -->|それ以外| I[エラーログの出力と空の辞書の返却]
      A -->|search_business_discovery| J[Instagram Graph API にリクエスト]
      J --> K[レスポンスの確認]
      K -->|ステータスコードが200| L[レスポンスの返却]
      K -->|それ以外| M[エラーログの出力と空の辞書の返却]
   ```

### Instagram Class

   ```mermaid
   graph TB
      N[Instagram クラスの初期化] --> O[InstagramAPI クラスの初期化]
      N -->|save_json| P[JSON ファイルの保存]
      N -->|read_json| Q[JSON ファイルの読み込み]
      N -->|save_csv| R[CSV ファイルの保存]
      N -->|count| S[投稿数のカウント]
      N -->|get_recent_media| T[最近のメディアの取得]
      N -->|get_hashtag_media| U[ハッシュタグメディアの取得]
      N -->|get_business_discovery| V[ビジネスディスカバリーの取得]
      N -->|run| W[全てのメソッドの実行]
   ```