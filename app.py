from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/value', methods=['GET'])
def get_value():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(
        api_url, headers={'Accept': 'application/vnd.github.v3+json'})

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch user data'}), response.status_code

    user_data = response.json()
    value = estimate_user_value(user_data)
    return jsonify({
        'value': value,
        'avatar_url': user_data.get('avatar_url'),
        'login': user_data.get('login'),
        'public_repos': user_data.get('public_repos'),
        'followers': user_data.get('followers'),
        'name': user_data.get('name'),
        'contributions': get_contributions(username)
    })


def estimate_user_value(user_data):
    followers = user_data.get('followers', 0)
    public_repos = user_data.get('public_repos', 0)
    return followers * 10 + public_repos * 5


def get_contributions(username):
    # Puedes implementar una lógica más precisa para obtener contribuciones
    # Para simplificar, vamos a sumar el número de commits de todos los repositorios públicos
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(
        repos_url, headers={'Accept': 'application/vnd.github.v3+json'})
    if repos_response.status_code != 200:
        return 0
    repos = repos_response.json()
    total_commits = 0
    for repo in repos:
        commits_url = repo['commits_url'].replace('{/sha}', '')
        commits_response = requests.get(
            commits_url, headers={'Accept': 'application/vnd.github.v3+json'})
        if commits_response.status_code == 200:
            total_commits += len(commits_response.json())
    return total_commits


if __name__ == '__main__':
    app.run(debug=True)
