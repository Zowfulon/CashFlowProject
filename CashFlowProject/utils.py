import datetime


def get_attributes(data):
    """Вспомогательный метод, собирающий все табы при подзагрузке и
    Post запросе"""
    final_data = {
        'money_type': data.get('money_type', None),
        'status': data.get('status', None),
        'category': data.get('category', None),
        'subcategory': data.get('subcategory', None),
        'date_gte': data.get('date_gte') if data.get('date_gte') != '' else None,
        'date_lte': data.get('date_lte') if data.get('date_lte') != '' else None
    }
    return final_data


def get_filtered_queryset(queryset, get_data):
    """Вспомогательный метод фильтрация списка записей.
    Вынесена отдельно, так как идентичный блок используется в двух функциях"""
    if get_data['status']:
        queryset = queryset.filter(status__slug=get_data['status'])
    if get_data['money_type']:
        queryset = queryset.filter(
            money_type__slug=get_data['money_type'])
        if get_data['category']:
            queryset = queryset.filter(category__slug=get_data['category'])
            if get_data['subcategory']:
                queryset = queryset.filter(
                    subcategory__slug=get_data['subcategory'])
    if get_data['date_gte']:
        date_gte = datetime.datetime.strptime(
            get_data['date_gte'], '%Y-%m-%d')
        queryset = queryset.filter(date_created__gte=date_gte)
    if get_data['date_lte']:
        date_lte = datetime.datetime.strptime(
            get_data['date_lte'], '%Y-%m-%d')
        queryset = queryset.filter(date_created__lte=date_lte)
    queryset = queryset.select_related('status', 'subcategory')
    return queryset


def get_new_parameters(data):
    """Собирает новую url для заданных параметров"""
    url_items = []
    if data['status']:
        url_items.append(f'status={data["status"]}')
    if data['money_type']:
        url_items.append(f'money_type={data["money_type"]}')
        if data['category']:
            url_items.append(f'category={data["category"]}')
            if data['subcategory']:
                url_items.append(f'subcategory={data["subcategory"]}')
    if data['date_gte']:
        url_items.append(f'date_gte={data["date_gte"]}')
    if data['date_lte']:
        url_items.append(f'date_lte={data["date_lte"]}')
    final_url = '&'.join(item for item in url_items)
    if final_url != '':
        final_url = '?' + final_url
    return final_url
