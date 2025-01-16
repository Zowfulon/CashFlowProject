import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic

from CashFlowProject.utils import get_attributes, get_filtered_queryset, \
    get_new_parameters, all_filters_active
from money_addition_notes.models import MoneyAdditionNote, MoneyAdditionType, \
    MoneyAdditionCategory, MoneyAdditionSubCategory, MoneyAdditionStatus


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
        'notes_page/notes_table.html',
        context={"notes": notes, 'user': request.user})
    response_data = {'html_data': html_data, 'new_url': new_url}
    return JsonResponse(response_data, content_type='application/json')


def change_tabs(request):
    """Метод, возвращающий отфильтрованные категории/подкатегории
       на основе изменения выбраных родителских групп
       Работает как на главной странице, так и на странице изменения и
       создания записи"""
    data = request.POST
    method = data.get('method')
    parent_slug = data.get('parent_slug')
    response_method = 'category'
    if method == 'money_type':
        filter_data = MoneyAdditionCategory.objects.filter(
                money_type__slug=parent_slug)
        template_name = 'includes/category_item.html'
    else:
        filter_data = MoneyAdditionSubCategory.objects.filter(
                money_category__slug=parent_slug)
        template_name = 'includes/subcategory_item.html'
        response_method = 'sub' + method
    html_data = render_to_string(
        template_name, context={'filtered_data': filter_data})
    response_data = {'response_method': response_method, 'html_data': html_data}
    return JsonResponse(response_data, content_type='application/json')


class NotesDetailView(generic.DetailView):
    """Детальная страница записи с формой и возможностью сохранить
       изменения и удалить запись"""
    model = MoneyAdditionNote
    template_name = 'notes_edit/note_edit_form.html'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Редактировать запись',
            'statuses': MoneyAdditionStatus.objects.all(),
            'money_types': MoneyAdditionType.objects.all(),
            'categories': MoneyAdditionCategory.objects.filter(
                money_type=self.get_object().money_type),
            'subcategories': MoneyAdditionSubCategory.objects.filter(
                money_category=self.get_object().category)

        })
        return context

    def post(self, request, **kwargs):
        note = self.get_object()
        data = {'success': True, 'message': 'Ваши данные успешно обновлены'}
        if request.POST.get('edit_type') == 'delete':
            note.delete()
        else:
            post_data = get_attributes(request.POST, 'edit')
            if not all_filters_active(post_data):
                data = {
                    'success': False,
                    'message': 'Произошла ошибка. Все поля, за исключением '
                               'комментария, являются обязательными'}
            else:
                note.date_created = datetime.datetime.strptime(
                    post_data['date_created'], '%Y-%m-%d')
                note.status = MoneyAdditionStatus.objects.get(
                    slug=post_data['status'])
                note.subcategory = MoneyAdditionSubCategory.objects.get(
                    slug=post_data['subcategory'])
                note.category = note.subcategory.money_category
                note.money_type = note.category.money_type
                note.comment = post_data['comment']
                note.money_value = float(post_data['money_value'])
                note.save()
        return JsonResponse(data)


class NoteCreateView(generic.TemplateView):
    """Страница создания записи"""
    template_name = 'notes_edit/note_edit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Создание записи',
            'statuses': MoneyAdditionStatus.objects.all(),
            'money_types': MoneyAdditionType.objects.all(),
            'today': datetime.datetime.today().date()
        })
        return context

    def post(self, request, **kwargs):
        post_data = get_attributes(request.POST, 'edit')
        data = {'success': True, 'message': 'Ваши данные успешно обновлены'}
        if not all_filters_active(post_data):
            data = {
                'success': False,
                'message': 'Произошла ошибка. Все поля, за исключением '
                           'комментария, являются обязательными'}
        else:
            subcategory = MoneyAdditionSubCategory.objects.get(slug=post_data['subcategory'])
            MoneyAdditionNote.objects.create(
                date_created=datetime.datetime.strptime(
                    post_data['date_created'], '%Y-%m-%d'),
                status=MoneyAdditionStatus.objects.get(slug=post_data['status']),
                subcategory=subcategory, category=subcategory.money_category,
                money_type=subcategory.money_category.money_type,
                money_value=float(post_data['money_value']),
                comment=post_data['comment'])
        return JsonResponse(data)
