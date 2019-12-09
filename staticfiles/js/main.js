document.addEventListener('click', function(event) {
  let e = document.getElementById('cat_nav');
  let menu = document.getElementById('menu_header');
  if (e.contains(event.target)) {
      e.classList.toggle('open');
  } else if (menu.contains(event.target)) {
      document.getElementById('base_wrapper').classList.toggle('open');
  } else {
      e.classList.remove('open');
  }
});
