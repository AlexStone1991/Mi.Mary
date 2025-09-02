# core/context_processors.py
from django.urls import reverse


def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {
            "name": "Главная",
            "url": reverse("landing") + "#top",
            "icon_class": "bi-house",
        },
        {
            "name": "Услуги",
            "url": reverse("landing") + "#services_list",
            "icon_class": "bi-scissors",
        },
        {
            "name": "Отзывы",
            "url": reverse("landing") + "#reviews",
            "icon_class": "bi-chat-dots",
        },
    ]

    staff_menu = [
        {
            "name": "Заявки",
            "url": reverse("orders"),
            "icon_class": "bi-clipboard-data",
        },
    ]

    return {"menu_items": menu, "menu_staff_items": staff_menu}
