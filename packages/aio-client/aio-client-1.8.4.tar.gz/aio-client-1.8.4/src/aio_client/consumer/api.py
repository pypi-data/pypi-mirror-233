# coding: utf-8
from django.forms.models import model_to_dict

from aio_client.base import RequestLog

from .exceptions import RequestNotFound
from .helpers import consumer_post_request
from .models import GetConsumerResponse
from .models import PostConsumerRequest


def push_request(message):
    """Передача сообщения на запрос услуги.

    :param message: Запись aio_client.provider.models.PostProviderRequest
    :return: Инстанс класса requests.models.Response
    """
    assert isinstance(message, PostConsumerRequest)
    response = consumer_post_request(message)
    return response


def get_response(message_id):
    """Получение ответа от СМЭВ на Запрос услуги.

    :param str message_id: Идентификатор сообщения, котрое РИС посылает в
        теге message_id при вызове api.push_request
    :return: Словарь со списком полей GetProviderReceipt.LIST_AIO_FIELDS
    """
    qs_response = PostConsumerRequest.objects.filter(
        message_id=message_id, request_id__state=RequestLog.SENT)
    if not qs_response.exists():
        raise RequestNotFound(
            message=RequestNotFound.DEFAULT_MSG % message_id)

    response = GetConsumerResponse.objects.filter(
        origin_message_id=message_id).order_by('id').last()
    if not response:
        return None
    return model_to_dict(response, GetConsumerResponse.LIST_AIO_FIELDS)


def get_responses(message_type=None):
    """Получение всех ответов от СМЭВ.

    :param message_type: Вид сведений, необязательный параметр,
        если не передается, отдаем все запросы
    :return: Список запросов к РИС как к поставщику услуг
    """
    qs = GetConsumerResponse.objects.exclude(
        state=GetConsumerResponse.SENT)
    if message_type:
        qs = qs.filter(message_type=message_type)
    result = tuple(qs.values('id', *GetConsumerResponse.LIST_AIO_FIELDS))
    GetConsumerResponse.objects.filter(
        id__in=[r['id'] for r in result]
    ).update(state=GetConsumerResponse.SENT)
    return result


def set_error_responses(origin_message_ids):
    """Указывает признак ошибки при обработке сообщения.

    Применяется для повторного получения сообщения в get_responses.

    :param origin_message_ids: Список origin_message_id
    :return: Количество измененных записей
    """
    assert isinstance(origin_message_ids, list)
    qs = GetConsumerResponse.objects.filter(
        origin_message_id__in=origin_message_ids)
    return qs.update(state=GetConsumerResponse.ERROR)
