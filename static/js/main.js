function estimateValue() {
  var username = document.getElementById('username').value;

  // Mostrar indicador de carga
  document.getElementById('loading').classList.remove('hidden');

  // Realizar la petición AJAX a la API de GitHub
  fetch(`https://api.github.com/users/${username}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }
      return response.json();
    })
    .then(data => {
      // Ocultar indicador de carga
      document.getElementById('loading').classList.add('hidden');

      // Mostrar resultados
      document.getElementById('result').classList.remove('hidden');

      // Actualizar los elementos con los datos del usuario
      document.getElementById('avatar').src = data.avatar_url;
      document.getElementById('username_display').innerText = data.name || data.login;
      document.getElementById('username_link').href = `https://github.com/${data.login}`;
      document.getElementById('repos').innerText = `Total Repos: ${data.public_repos}`;
      document.getElementById('followers').innerText = `Followers: ${data.followers}`;

      // Como 'contributions' y 'value' no están en la respuesta de la API de GitHub, los puedes eliminar o asignarles valores por defecto
      document.getElementById('contributions').innerText = `Contributions: No data`; // GitHub no proporciona directamente este dato
      document.getElementById('value').innerText = `$ Not available`;

      // Generar gráfico de contribuciones
      document.getElementById('contributions_graph').src = `https://ghchart.rshah.org/${data.login}`;
    })
    .catch(error => {
      // Ocultar indicador de carga
      document.getElementById('loading').classList.add('hidden');

      // Mostrar mensaje de error
      document.getElementById('error').classList.remove('hidden');
      console.error('Error:', error.message);
    });
}
