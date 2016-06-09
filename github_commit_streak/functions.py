import requests
import datetime


def json_request(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ConnectionError(response.json())

    return response.json()


def calculate(api_key, email, verbose=False):
    auth_header = {'Authorization': 'token {0}'.format(api_key)}

    repos = json_request('https://api.github.com/user/repos', auth_header)

    dates_with_commits = set()

    for repo in repos:
        if verbose:
            print('Fetching commits for {0}...'.format(repo['name']))

        commits_url = repo['commits_url'].replace('{/sha}', '') + '?author=' + email
        commits = json_request(commits_url, auth_header)

        for commit in commits:
            try:
                if len(commit['parents']) <= 1:
                    date = commit['commit']['author']['date'][:10]
                    dates_with_commits.add(date)
            except TypeError as e:
                # Something missing from commit, disregard it.
                pass

    count = 0
    date = datetime.date.today()
    while date.strftime('%Y-%m-%d') in dates_with_commits:
        count = count + 1
        date = date - datetime.timedelta(days=1)

    return count
