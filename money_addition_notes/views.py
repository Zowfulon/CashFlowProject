from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import generic

from CashFlowProject.utils import get_attributes, get_filtered_queryset, \
    get_new_parameters
from money_addition_notes.models import MoneyAdditionNote, MoneyAdditionCategory, \
    MoneyAdditionSubCategory, MoneyAdditionStatus, MoneyAdditionType


# Create your views here.


class MoneyAdditionNotesView(generic.ListView):
    """View-класс главной страницы. В данном классе расширены 2 функции
    get_queryset и get_context_data, позволяющие подгружать"""
    model = MoneyAdditionNote
    template_name = 'notes_page/notes_main_page.html'
    context_object_name = 'notes'

    def get_queryset(self):
        """Расширенный метод get_queryset, который отфильтровывает записи
        при загрузке страницы (если есть в url Get параметры)"""
        queryset = super(MoneyAdditionNotesView, self).get_queryset()
        get_data = get_attributes(self.request.GET)
        queryset = get_filtered_queryset(queryset, get_data)
        return queryset

    def get_context_data(self, **kwargs):
        notes = self.get_queryset()
        context = super(MoneyAdditionNotesView, self).get_context_data(**kwargs)
        context.update({'notes': notes})
        filters = get_attributes(self.request.GET)
        if filters['money_type']:
            filtered_categories = MoneyAdditionCategory.objects.filter(
                money_type__slug=filters['money_type'])
            context.update({'filtered_categories': filtered_categories})
            if filters['category']:
                filtered_subcat = MoneyAdditionSubCategory.objects.filter(
                    money_category__slug=filters['category'])
                context.update({'filtered_subcategories': filtered_subcat})
        context.update({
            'filters': filters, 'statuses': MoneyAdditionStatus.objects.all(),
            'money_types': MoneyAdditionType.objects.all()
        })
        return context


def notes_filter(request):
    """Meтод, возвращающий отрендеренный блок с таблицей на основе
       активных фильтров"""
    post_data = get_attributes(request.POST)
    new_url = get_new_parameters(post_data)
    notes = get_filtered_queryset(
        queryset=MoneyAdditionNote.objects.all(), get_data=post_data)
    html_data = render_to_string(
        'notes_page/notes_table.html', context={"notes": notes})
    return JsonResponse({'html_data': html_data, 'new_url': new_url})


def change_tabs(request):
    """Метод, возвращающий отфильтрованные категории/подкатегории
       на основе изменения выбраных родителских групп
       Работает как на главной странице, так и на странице изменения и
       создания записи"""
    data = request.POST
    method = data.get('method')
    parent_slug = data.get('parent_slug')
    if method == 'type':
        filter_data = MoneyAdditionCategory.objects.filter(
                money_type__slug=parent_slug)
    else:
        filter_data = MoneyAdditionSubCategory.objects.filter(
                category__slug=parent_slug)
    return JsonResponse({'method': method,'filter_data': filter_data})


class NotesDetaitView(generic.DetailView):
    pass
