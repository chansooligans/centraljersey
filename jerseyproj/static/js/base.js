const dropdownButton = document.querySelector('.dropdown-toggle');
const dropdownItems = document.querySelectorAll('.dropdown-item');
const iframe = document.querySelector('iframe');

dropdownItems.forEach(item => {
  item.addEventListener('click', function() {
    console.log(123)
    iframe.src = this.getAttribute('value') + '/';
  });
});