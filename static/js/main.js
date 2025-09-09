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
