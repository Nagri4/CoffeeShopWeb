"""
Тимчасові дані (заглушки). На етапі IV ці списки замінить база даних SQLite
з таблицями categories, menu_items, users та reservations.
"""

CATEGORIES = [
    {"id": 1, "name": "Кава", "slug": "coffee"},
    {"id": 2, "name": "Чай", "slug": "tea"},
    {"id": 3, "name": "Десерти", "slug": "desserts"},
    {"id": 4, "name": "Випічка", "slug": "bakery"},
    {"id": 5, "name": "Сніданки", "slug": "breakfast"},
]

# image — назва файлу в static/img/menu/ (якщо файлу немає, показується кольорова заглушка)
MENU_ITEMS = [
    {"id": 1, "category_id": 1, "name": "Еспресо", "description": "Коротка й насичена класика, 100% арабіка",
     "details": "Подвійна порція еспресо на зерні власного обсмаження. Ноти темного шоколаду й карамелі, щільна крема.",
     "price": 55, "volume": "30 мл", "calories": "5 ккал", "label": "Хіт", "image": "espresso.jpg",
     "is_available": True, "popularity": 95},
    {"id": 2, "category_id": 1, "name": "Капучино", "description": "Подвійний еспресо, молоко, щільна пінка",
     "details": "Подвійний еспресо з молоком і щільною оксамитовою пінкою. Готуємо на зерні власного обсмаження — бразилія та колумбія, ноти горіха й молочного шоколаду.",
     "price": 75, "volume": "250 мл", "calories": "120 ккал", "label": "Хіт", "image": "cappuccino.jpg",
     "is_available": True, "popularity": 100},
    {"id": 3, "category_id": 1, "name": "Лате на вівсяному", "description": "Ніжний смак без лактози",
     "details": "Еспресо з вівсяним молоком — м'який, трохи солодкуватий смак без лактози.",
     "price": 90, "volume": "350 мл", "calories": "140 ккал", "label": "Новинка", "image": "latte-oat.jpg",
     "is_available": True, "popularity": 80},
    {"id": 4, "category_id": 1, "name": "Раф лавандовий", "description": "Вершки, ваніль, лавандовий сироп",
     "details": "Еспресо, збитий з вершками, ванільним цукром і домашнім лавандовим сиропом.",
     "price": 95, "volume": "300 мл", "calories": "260 ккал", "label": "", "image": "raf-lavender.jpg",
     "is_available": True, "popularity": 70},
    {"id": 5, "category_id": 1, "name": "Флет вайт", "description": "Більше кави, менше молока",
     "details": "Подвійний ристрето з тонким шаром мікропіни — яскравий кавовий смак.",
     "price": 80, "volume": "180 мл", "calories": "90 ккал", "label": "", "image": "flat-white.jpg",
     "is_available": True, "popularity": 65},
    {"id": 6, "category_id": 1, "name": "Американо", "description": "Еспресо, розбавлений гарячою водою",
     "details": "Класичний американо на подвійному еспресо. За бажанням — з молоком.",
     "price": 60, "volume": "300 мл", "calories": "10 ккал", "label": "", "image": "americano.jpg",
     "is_available": True, "popularity": 75},
    {"id": 7, "category_id": 2, "name": "Чай з чебрецем", "description": "Чорний листовий чай, мед окремо",
     "details": "Чорний цейлонський чай із сушеним чебрецем. Мед подаємо окремо.",
     "price": 60, "volume": "400 мл", "calories": "5 ккал", "label": "", "image": "tea-thyme.jpg",
     "is_available": True, "popularity": 55},
    {"id": 8, "category_id": 2, "name": "Матча лате", "description": "Японський зелений чай з молоком",
     "details": "Церемоніальна матча, збита з молоком. Можна на рослинному молоці.",
     "price": 95, "volume": "300 мл", "calories": "150 ккал", "label": "Новинка", "image": "matcha.jpg",
     "is_available": True, "popularity": 50},
    {"id": 9, "category_id": 3, "name": "Сирники", "description": "Зі сметаною та ягідним соусом",
     "details": "Домашні сирники з кисломолочного сиру, подаємо зі сметаною і ягідним соусом.",
     "price": 110, "volume": "220 г", "calories": "420 ккал", "label": "Хіт", "image": "syrnyky.jpg",
     "is_available": True, "popularity": 90},
    {"id": 10, "category_id": 3, "name": "Чізкейк Нью-Йорк", "description": "Класичний, з вишневим топінгом",
     "details": "Щільний вершковий чізкейк на пісочній основі з вишневим топінгом.",
     "price": 120, "volume": "150 г", "calories": "390 ккал", "label": "", "image": "cheesecake.jpg",
     "is_available": True, "popularity": 60},
    {"id": 11, "category_id": 4, "name": "Круасан", "description": "Листкове тісто на вершковому маслі",
     "details": "Французький круасан на вершковому маслі 82%. Печемо щоранку.",
     "price": 70, "volume": "80 г", "calories": "330 ккал", "label": "", "image": "croissant.jpg",
     "is_available": False, "popularity": 85},
    {"id": 12, "category_id": 5, "name": "Гранола з йогуртом", "description": "Домашня гранола, йогурт, ягоди",
     "details": "Запечена гранола з горіхами, грецький йогурт і свіжі ягоди.",
     "price": 125, "volume": "250 г", "calories": "380 ккал", "label": "", "image": "granola.jpg",
     "is_available": True, "popularity": 40},
]

BOOKING_TIMES = [f"{h:02d}:{m:02d}" for h in range(8, 21) for m in (0, 30)]

MY_RESERVATIONS = [
    {"date": "24.10.2026", "time": "18:30", "guests": 2, "comment": "Біля вікна", "status": "confirmed"},
    {"date": "31.10.2026", "time": "10:00", "guests": 4, "comment": "", "status": "pending"},
    {"date": "12.10.2026", "time": "19:00", "guests": 2, "comment": "", "status": "done"},
]
