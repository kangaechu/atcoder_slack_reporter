atcoder_slack_reporter
====

AtCoderの回答状況をSlackに通知

## Description

複数人でAtCoderをしている場合、他の人がどのくらい進んだかが気になりますね。
このツールはSlackに正答状況を定期的に通知してくれます。

## Requirement

Python3

## Installation


### 依存パッケージのインストール

```bash
# pip3 install -r requirements.txt
```

### 設定の変更

 コンテスト名(contest)、監視対象ユーザ名(users)、SlackのWebhook URL (slack)を変更します。
```python
    standings = Standings(contest='abc101', users=['user01', 'user02'])
    slack = Slack('SLACK_INTEGRATION_URL')
```

## Usage

```bash
# python atcoder_slack_reporter.py
```

## Licence

MIT

## Author

[kangaechu](https://github.com/kangaechu)
