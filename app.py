import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
# Obtén tu token de acceso personal de las variables de entorno o configúralo directamente
github_token = os.getenv('GITHUB_TOKEN')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/value/repos', methods=['GET'])
def get_value_by_repos():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    user_data = fetch_user_data(username)
    if 'error' in user_data:
        return jsonify(user_data), 400

    value = estimate_user_value_by_repos(user_data)
    return jsonify({**user_data, 'value': value, 'total_stars': calculate_total_stars(username)})


@app.route('/value/stars', methods=['GET'])
def get_value_by_stars():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    user_data = fetch_user_data(username)
    if 'error' in user_data:
        return jsonify(user_data), 400

    value = estimate_user_value_by_stars(username)
    return jsonify({**user_data, 'value': value, 'total_stars': calculate_total_stars(username)})


@app.route('/value/followers_repos', methods=['GET'])
def get_value_by_followers_repos():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    user_data = fetch_user_data(username)
    if 'error' in user_data:
        return jsonify(user_data), 400

    value = estimate_user_value_by_followers_repos(user_data)
    return jsonify({**user_data, 'value': value, 'total_stars': calculate_total_stars(username)})


@app.route('/value/total', methods=['GET'])
def get_total_value():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    user_data = fetch_user_data(username)
    if 'error' in user_data:
        return jsonify(user_data), 400

    value_repos = estimate_user_value_by_repos(user_data)
    value_stars = estimate_user_value_by_stars(username)
    value_followers_repos = estimate_user_value_by_followers_repos(user_data)
    total_value = value_repos + value_stars + value_followers_repos

    return jsonify({
        **user_data,
        'value': total_value,
        'value_repos': value_repos,
        'value_stars': value_stars,
        'value_followers_repos': value_followers_repos,
        'total_stars': calculate_total_stars(username)
    })


def fetch_user_data(username):
    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(
        api_url,
        headers={
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    if response.status_code != 200:
        return {'error': 'Failed to fetch user data  {response.status_code}'}

    user_data = response.json()
    user_data['contributions'] = get_contributions(username)
    return user_data


def estimate_user_value_by_repos(user_data):
    return user_data.get('public_repos', 0) * 20


def estimate_user_value_by_stars(username):
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(
        repos_url,
        headers={
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    if repos_response.status_code != 200:
        return 0
    repos = repos_response.json()
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    return total_stars * 5


def estimate_user_value_by_followers_repos(user_data):
    followers = user_data.get('followers', 0)
    public_repos = user_data.get('public_repos', 0)
    return followers * 10 + public_repos * 5


def get_contributions(username):
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(
        repos_url,
        headers={
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    if repos_response.status_code != 200:
        return 0
    repos = repos_response.json()
    total_commits = 0
    for repo in repos:
        commits_url = repo['commits_url'].replace('{/sha}', '')
        commits_response = requests.get(
            commits_url,
            headers={
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        if commits_response.status_code == 200:
            total_commits += len(commits_response.json())
    return total_commits


def calculate_total_stars(username):
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(
        repos_url,
        headers={
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    if repos_response.status_code != 200:
        return 0
    repos = repos_response.json()
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
    return total_stars


if __name__ == '__main__':
    app.run(debug=True)
