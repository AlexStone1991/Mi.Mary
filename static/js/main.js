// Файл: static/js/main.js

document.addEventListener("DOMContentLoaded", function() {

    // Функция для анимации при прокрутке
    const animateOnScroll = () => {
        const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                    // Опционально: перестать наблюдать после одного срабатывания
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1 // Анимация начнется, когда элемент виден на 10%
        });

        elementsToAnimate.forEach(element => {
            observer.observe(element);
        });
    };

    // Вызываем нашу функцию
    animateOnScroll();
});
// Добавь в конец скрипта
document.addEventListener('DOMContentLoaded', function() {
    // Фикс для мобильного скролла
    function fixMobileScroll() {
        if (window.innerWidth < 768) {
            document.documentElement.style.overflowX = 'hidden';
            document.body.style.overflowX = 'hidden';
        }
    }
    
    fixMobileScroll();
    window.addEventListener('resize', fixMobileScroll);
    
    // Дополнительно: закрываем меню при клике на ссылку
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            const navbar = document.querySelector('.navbar-collapse');
            if (navbar.classList.contains('show')) {
                bootstrap.Collapse.getInstance(navbar).hide();
            }
        });
    });
});