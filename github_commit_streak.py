import requests
import datetime


EMAIL = 'mats@hgbrg.se'


def calculate(API_KEY):
    REQUEST_HEADER = {'Authorization': 'token {0}'.format(API_KEY)}
    repos = requests.get('https://api.github.com/user/repos', headers=REQUEST_HEADER)
    if repos.status_code != 200:
        print('Repos request failed with status code {0}: {1}'.format(repos.status_code, repos.json()['message']))
        return

    dates_with_commits = set()

    for repo in repos.json():
        commits_url = repo['commits_url'].replace('{/sha}', '') + '?author=' + EMAIL
        commits = requests.get(commits_url, headers=REQUEST_HEADER)

        print(repo['name'])

        if commits.status_code != 200:
            print('Commits request failed with status code {0}. {1}'.format(commits.status_code, repos.json()['message']))
            return

        for commit in commits.json():
            try:
                if len(commit['parents']) <= 1:
                    date = commit['commit']['author']['date'][:10]
                    dates_with_commits.add(date)
            except TypeError as e:
                print(e)
                print(commit)
                pass

    count = 0
    date = datetime.date.today()
    while True:
        if date.strftime('%Y-%m-%d') in dates_with_commits:
            count = count + 1
            date = date - datetime.timedelta(days=1)
        else:
            break

    return count
