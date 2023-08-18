  // Exibir o álbum após a animação
  const albumContainer = document.querySelector('.album-container')

  function showAlbum() {
    document.querySelector('.album-content').style.opacity = '1';

    setTimeout(() => {
        albumContainer.classList.add('centered');
      }, 0); // Aguarde o tempo da animação antes de centralizar
  }

  window.onload = showAlbum;

  const albumContainers = document.querySelectorAll('.clickable');

  albumContainers.forEach(albumContainer => {
    albumContainer.addEventListener('click', () => {
      albumContainer.classList.add('expanded');
    });
  });
  
