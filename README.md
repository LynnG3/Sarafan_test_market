# Sarafan_test_market - Django проект интернет магазина.

## Структура, возможности и эндпойнты проекта:

В проекте реализованы модели продукта, категории, подкатегории, заказа (товар-в корзине)

- Категории и подкатегории имеют наименование, slug-имя, изображение
- Подкатегории связаны с родительской категорией
- Эндпоинт для просмотра всех категорий с подкатегориями, с пагинацией:
  # /api/categories/

- Продукты относятся к определенной подкатегории и, соответственно категории,
  имеют наименование, slug-имя, изображение в 3-х размерах, цену
- Реализована возможность добавления, изменения, удаления продуктов в админке.
- Реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке.
- Реализована автоматическая генерация изображений
  в размерах medium и small на основе загруженного исходного изображения.
  Настроить размеры изображений можнно в константах : backend/market_backend/constants.py
- Эндпоинт вывода продуктов с пагинацией:
  # /api/products/
  Каждый продукт в выводе имеет поля: наименование, slug, категория, подкатегория, цена, список изображений
-	Эндпоинт добавления товара:
  # /api/purchase/
  изменения (изменение количества), удаления продукта в корзине:
  # /api/purchase/{id}/
- Эндпоинт вывода  состава корзины с подсчетом количества товаров
  и суммы стоимости товаров в корзине:
  # /api/purchase/get_shoping_cart/
-	Эндпойнт полной очистки корзины:
  # /api/purchase/clear_cart/
- Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь - применено разрешение AllowAny
-	Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь
  и только со своей корзиной - применено разрешение IsAuthenticated и кастомное разрешение IsOwner 
-	Реализована авторизация по токену с помощью Djoser

    	  
## Как запустить проект:

Клонировать репозиторий к себе на компьютер и перейти в директорию с проектом:
```bash
git clone git@github.com:LynnG3/Sarafan_test_market.git
cd Sarafan_test_market
```
Для проекта создать и активировать виртуальное окружение, установить зависимости:
__для windows:__
```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend
```
__для linux:__
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend
```
Выполнить миграции и запустить локальный сервер :
```bash
python manage.py migrate
python manage.py runserver
```
-	Автоматическая документация будет доступна после локального запуска проекта по адресу:
  ```bash
	http://127.0.0.1:8000/api/schema/docs/
  ```
## Технологии:
 - Django
 - DjangoRestFramework
 - Djoser
 - DRF Spectacular
 - Pillow
 - Python
 - sqlite3
   
### Автор: Полина Грунина, https://t.me/GrethenMorgan 
