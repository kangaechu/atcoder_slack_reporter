import json
import logging
from time import sleep

import requests

logger = logging.getLogger(__name__)

fmt = "%(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)

ATCODER_BASE_URL = 'https://beta.atcoder.jp/contests/##CONTEST_ID##/standings/json'


class Standings:
    contest = None
    users = []
    standings_prev = None
    standings = None

    def __init__(self, contest, users):
        self.contest = contest
        self.users = users
        self.standings = self.get_standings()

    def get_standings(self):
        """
        コンテストのJSONから順位などの情報を取得する
        :return:
        """
        url = ATCODER_BASE_URL.replace('##CONTEST_ID##', self.contest)
        response = requests.get(url)
        standings = response.json()
        target_standings = [s for s in standings['StandingsData'] if s['UserName'] in self.users]
        # 不要な情報を除去
        result = dict()
        for user in target_standings:
            questions = list()
            for question_name, question_result in user['TaskResults'].items():
                if question_result['Score'] > 0:
                    questions.append(question_name)
            result[user['UserName']] = set(questions)
        return result

    def update(self):
        """
        回答の状況を更新し、更新があったユーザと回答を返す
        :return: 更新のあったユーザと回答({'kangaechu': {'abc101_b'}})
        """
        self.standings_prev = self.standings
        self.standings = self.get_standings()

        result = dict()
        for username in self.standings.keys():
            if self.standings_prev[username] != self.standings[username]:
                result[username] = self.standings_prev[username] ^ self.standings[username]
        return result


class Slack:
    webhook_url: str

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def post(self, message):
        payload = {
            'text': message,
            'username': 'atcoder',
            'icon_emoji': ':shamrock:',
            'channel': '#competitive_program',
        }
        response = requests.post(self.webhook_url, data=json.dumps(payload))
        logging.info(message)

    def post_standings(self, standings):
        """
        standingの各要素に対し、slackにpost
        :param standings:
        :return:
        """
        for user, tasks in standings.items():
            for task in tasks:
                message = '{}が{}に正解しました！'.format(user, task)
                self.post(message)


if __name__ == '__main__':
    standings = Standings(contest='abc101', users=['user01', 'user02'])
    slack = Slack('SLACK_INTEGRATION_URL')

    while True:
        update_standings = standings.update()
        slack.post_standings(update_standings)
        sleep(60)
