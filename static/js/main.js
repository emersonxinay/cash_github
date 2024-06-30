async function estimateValue() {
  const username = document.getElementById('username').value;
  const response = await fetch(`/value?username=${username}`);
  const data = await response.json();
  if (response.ok) {
    document.getElementById('avatar').src = data.avatar_url;
    document.getElementById('username_display').innerText = data.name || data.login;
    document.getElementById('username_link').href = `https://github.com/${data.login}`;
    document.getElementById('repos').innerText = `Total Stars: ${data.public_repos}`;
    document.getElementById('followers').innerText = `Total Followers: ${data.followers}`;
    document.getElementById('contributions').innerText = `Total Contributions: ${data.contributions}`;
    document.getElementById('value').innerText = `$ ${data.value}`;
    document.getElementById('contributions_graph').src = `https://ghchart.rshah.org/${data.login}`;
    document.getElementById('result').style.display = 'block';
  } else {
    document.getElementById('result').innerText = `Error: ${data.error}`;
  }
}
