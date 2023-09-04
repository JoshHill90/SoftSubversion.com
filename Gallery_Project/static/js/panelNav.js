document.addEventListener("DOMContentLoaded", function(event) {
    const toggleIcons = document.querySelectorAll('.header_toggle');
    const nav = document.getElementById('nav-bar');
    const bodypd = document.getElementById('body-pd');
    const headerpd = document.getElementById('header');

    toggleIcons[0].addEventListener('click', () => {
        nav.classList.toggle('show');
        bodypd.classList.toggle('body-pd');
        headerpd.classList.toggle('body-pd');
    });

    const linkColor = document.querySelectorAll('.nav_link');

    function colorLink() {
        linkColor.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    }

    linkColor.forEach(l => l.addEventListener('click', colorLink));
});