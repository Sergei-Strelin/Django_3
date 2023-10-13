import logging
import datetime

from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from shop_app.models import Client, Order, Goods, Image
from shop_app.forms import EditGoodForm, ImageForm

logger = logging.getLogger(__name__)


def get_clients(request):
    clients = Client.objects.all()
    context = '\n'.join(str(client) for client in clients)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_goods(request):
    goods = Goods.objects.all()
    context = '\n'.join(str(g) for g in goods)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_orders(request):
    orders = Order.objects.all()
    context = '\n'.join(str(order) for order in orders)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_orders_by_client_id(request, client_id: int):
    orders = Order.objects.filter(client_id=client_id)
    if orders:
        context = '\n'.join(str(order) for order in orders)
    else:
        context = f'У пользователя с id: {client_id} нет заказов'
    logger.info(f'context: {context}')
    return HttpResponse(context)


def delete_client(request, client_id: int):
    client = Client.objects.filter(pk=client_id)
    if client:
        client.delete()
        logger.info(f'Пользователь удален')
        return HttpResponse('Пользователь удален')
    else:
        logger.info(f'Пользователь не найден')
        return HttpResponse('Пользователь не найден')


def delete_goods(request, goods_id: int):
    goods = Goods.objects.filter(pk=goods_id)
    if goods:
        goods.delete()
        logger.info(f'Товар удален')
        return HttpResponse('Товар удален')
    else:
        logger.info(f'Товар не найден')
        return HttpResponse('Товар не найден')


def delete_order(request, order_id: int):
    order = Order.objects.filter(pk=order_id)
    if order:
        order.delete()
        logger.info(f'Заказ удален')
        return HttpResponse('Заказ удален')
    else:
        logger.info(f'Заказ не найден')
        return HttpResponse('Заказ не найден')


def edit_client_name(request, client_id: int, name: str):
    client = Client.objects.filter(pk=client_id).first()
    if client:
        client.name = name
        client.save()
        logger.info(f'Имя клиента изменено')
        return HttpResponse('Имя клиента изменено')
    else:
        logger.info(f'Клиент не найден')
        return HttpResponse('Клиент не найден')


def edit_goods_price(request, goods_id: int, price: int):
    goods = Goods.objects.filter(pk=goods_id).first()
    if goods:
        goods.price = price
        goods.save()
        logger.info(f'Цена товара изменена')
        return HttpResponse('Цена товара изменена')
    else:
        logger.info(f'Товар не найден')
        return HttpResponse('Товар не найден')


def edit_order_goods_id(request, order_id: int, goods_id: int):
    order = Order.objects.filter(pk=order_id).first()
    goods = Goods.objects.filter(pk=goods_id).first()
    if order:
        order.goods_id = goods
        order.save()
        return HttpResponse('Товар в заказе изменен')
    else:
        return HttpResponse('Такой заказ не найден')


def test(request):
    context = {
        'title': 'Тестовая страница',
        'pk': Client.objects.order_by('name')
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/test.html', context)


def get_client_goods(request, client_id: int):
    COUNT_DAYS = 7
    start = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS)
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client_id=client_id, create_at__gte=start)
    context = {
        'title': 'шаблон',
        'count_days': COUNT_DAYS,
        'client': client,
        'orders': orders,
        'text': f'http://127.0.0.1:8000/get_client_goods/'
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/client_goods.html', context)


def client_goods(request):
    title = 'шаблон'
    host = request.META["HTTP_HOST"]
    path = request.path
    text = f'{host}{path}'
    if request.method == "POST":
        client_id = request.POST['number']
        COUNT_DAYS = 7
        start = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS)
        client = Client.objects.get(id=client_id)
        orders = Order.objects.filter(client_id=client_id, create_at__gte=start)
        images = Goods.objects.all()
        url_path = f'{text}{client_id}'
        context = {
            'title': title,
            'count_days': COUNT_DAYS,
            'client': client,
            'orders': orders,
            'url_path': url_path,
            'images': images,
            'text': f'{text}'
        }
        logger.info(f'context: {context}')
        return render(request, 'shop_app/client_goods.html', context)
    else:
        context = {
            'title': title,
            'text': f'{text}'
        }
        logger.info(f'context: {context}')
        return render(request, 'shop_app/client_goods.html', context)


def main(request):
    context = {
        'title': 'Главная страница',
        'goods': Goods.objects.order_by('name', 'description')
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/index.html', context)


def get_catalog(request):
    title = "Каталог"
    goods = Goods.objects.all()
    context = {
        'title': title,
        'goods': goods,
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/catalog.html', context=context)


def contacts(request):
    title = "Контакты"
    clients = Client.objects.all()
    context = {
        'title': title,
        'clients': clients,
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/contacts.html', context)


def all_clients(request: HttpRequest) -> HttpResponse:
    clients_with_order_counts = Client.objects.annotate(order_count=Count("orders"))
    return render(
        request, "shop_app/index.html", context={"clients": clients_with_order_counts}
    )


def orders_by_client(request: HttpRequest, client_pk: int) -> HttpResponse:
    title = "orders_by_client"
    client = get_object_or_404(Client, pk=client_pk)
    orders = client.objects.all()
    all_goods_by_client = set()
    for order in orders:
        all_goods_by_client.update(order.goods.all())
    goods = sorted(list(all_goods_by_client), key=lambda good: good.pk, reverse=True)
    context = {
        'title': title,
        "client": client,
        "orders": orders,
        "goods": goods,
    }
    return render(request, "shop_app/orders_by_client.html", context=context)


def order_full(request: HttpRequest, order_pk: int) -> HttpResponse:
    title = "order_full"
    order = get_object_or_404(Order, pk=order_pk)
    goods = order.goods.all()
    context = {
        'title': title,
        "order": order,
        "goods": goods,
    }
    return render(request, "shop_app/order_full.html", context=context)


def good_full(request: HttpRequest, good_pk: int) -> HttpResponse:
    title = "good_full"
    good = get_object_or_404(Goods, pk=good_pk)
    context = {
        'title': title,
        "good": good,
    }
    return render(request, "shop_app/good_full.html", context=context)


def edit_good(request: HttpRequest, good_pk: int) -> HttpResponse:
    title = "форма"
    good = get_object_or_404(Goods, pk=good_pk)
    if request.method == "POST":
        form = EditGoodForm(request.POST, request.FILES)
        if form.is_valid():
            good.name = request.POST["title"]
            good.description = request.POST["description"]
            good.price = request.POST["price"]
            good.amount = request.POST["quantity"]
            if "image" in request.FILES:
                good.image = request.FILES["image"]
            good.save()
            img_obj = good.image
            return render(request, 'shop_app/edit_good.html', {'form': form, 'img_obj': img_obj})
        else:
            form = EditGoodForm()
            if form.is_valid():
                good.name = request.POST["title"]
                good.description = request.POST["description"]
                good.price = request.POST["price"]
                good.amount = request.POST["quantity"]
                if "image" in request.FILES:
                    good.image = request.FILES["image"]
                good.save()
            logger.info(f"Good {good.name} edited")
            return render(request, 'shop_app/edit_good.html', {'form': form})
            # return redirect("good_full", good_pk=good.pk)
    else:
        form = EditGoodForm(
            initial={
                "title": good.name,
                "description": good.description,
                "price": good.price,
                "quantity": good.amount,
            },
        )
    context = {
        'title': title,
        "form": form,
        "good": good,
    }
    return render(request, "shop_app/edit_good.html", context=context)


def get_edit_good(request: HttpRequest) -> HttpResponse:
    title = "форма"
    good = get_object_or_404(Goods, pk=1)
    if request.method == "POST":
        form = EditGoodForm(request.POST, request.FILES)
        if form.is_valid():
            good.name = request.POST["title"]
            good.description = request.POST["description"]
            good.price = request.POST["price"]
            good.amount = request.POST["quantity"]
            if "image" in request.FILES:
                good.image = request.FILES["image"]
            good.save()
            logger.info(f"Good {good.name} edited")
            return redirect("good_full", good_pk=good.pk)
    else:
        form = EditGoodForm(
            initial={
                "title": good.name,
                "description": good.description,
                "price": good.price,
                "quantity": good.amount,
            },
        )
    context = {
        'title': title,
        "form": form,
        "good": good,
    }
    return render(request, "shop_app/edit_good.html", context=context)


def upload_images(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/upload_images")
    else:
        form = ImageForm

    return render(request, 'shop_app/images.html', {'form': form})


def upload_images1(request):
    if request.method == 'GET':
        images = Image.objects.order_by('title')
        return render(request, "shop_app/images.html", {"images": images})