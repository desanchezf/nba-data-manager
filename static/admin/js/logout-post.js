/**
 * Cerrar sesión con POST (requerido en Django 4.1+).
 * Intercepta cualquier clic en "Log out" (menú usuario Jazzmin) y envía POST.
 */
(function() {
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function doLogoutPost(href) {
    var csrftoken = getCookie('csrftoken');
    var form = document.createElement('form');
    form.method = 'post';
    form.action = href.split('?')[0];
    form.style.display = 'none';
    if (csrftoken) {
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'csrfmiddlewaretoken';
      input.value = csrftoken;
      form.appendChild(input);
    }
    var next = href.match(/[?&]next=([^&]+)/);
    if (next) {
      var nextInput = document.createElement('input');
      nextInput.type = 'hidden';
      nextInput.name = 'next';
      nextInput.value = decodeURIComponent(next[1].replace(/\+/g, ' '));
      form.appendChild(nextInput);
    }
    document.body.appendChild(form);
    form.submit();
  }

  document.addEventListener('click', function(e) {
    var link = e.target && e.target.closest && e.target.closest('a[href*="logout"]');
    if (!link) return;
    e.preventDefault();
    e.stopPropagation();
    var href = link.getAttribute('href');
    if (href) doLogoutPost(href);
  }, true);
})();
