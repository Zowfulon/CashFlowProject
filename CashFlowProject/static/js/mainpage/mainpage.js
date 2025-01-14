function note_filter(data){
    $.ajax({
        url: '/filter/',
        type: 'POST',
        data: data,
        success: function (data) {
            $('.note-cards').html(data['html_data'])
            const current_url = document.location.href
            const new_url = current_url.split('?')[0] + data['new_url']
            window.history.pushState('', '', new_url)
        },
    })
}


$(document).ready(function () {
    $(document).on('click', '.note-filter-button', function (){
        const data = {
            'status': $('.status-item.active').data('slug'),
            'money_type': $('.money_type-item.active').data('slug'),
            'category': $('.category-item.active').data('slug'),
            'subcategory': $('.subcategory-item.active').data('slug'),
            'date_gte': $('.date_gte-item').val(),
            'date_lte': $('.date_lte-item').val()
        }
        note_filter(data)
    })
    $(document).on('click', '.note-refresh-button', function (){
        $('.subcategory-item.active').removeClass('active')
        const subcategory = $('.subcategory-filters')
        if (!subcategory.hasClass('hidden')){
            subcategory.addClass('hidden')
        }
        $('.category-item.active').removeClass('active')
        const category = $('.category-filters')
        if (!category.hasClass('hidden')) {
            category.addClass('hidden')
        }
        $('.money_type-item.active').removeClass('active')
        $('.status-item.active').removeClass('active')
        $('.date_gte-item').val('')
        $('.date_lte-item').val('')
        note_filter({})
        $('.status-input').text('Статус')
        $('.money_type-input').text('Тип')
        $('.category-input').text('Категория')
        $('.subcategory-input').text('Подкатегория')
    })
    $(document).on('click', '.status-item', function (){
        $('.status-item.active').removeClass('active')
        $(this).addClass('active')
        $('.status-input').text($(this).text())
    })
    $(document).on('click', '.money_type-item', function (){
        $('.category-input').text('Категория')
        $('.subcategory-input').text('Подкатегория')
        $('.money_type-item.active').removeClass('active')
        $(this).addClass('active')
        $('.money_type-input').text($(this).text())
        const subcategory = $('.subcategory-filters')
        if (!subcategory.hasClass('hidden')){
            subcategory.addClass('hidden')
        }
        const category = $('.category-filters')
        if (category.hasClass('hidden')) {
            category.removeClass('hidden')
        }
        $('.subcategory-item_container').html('')
        change_tabs('money_type', $(this).data('slug'))
    })
    $(document).on('click', '.category-item', function (){
        $('.subcategory-input').text('Подкатегория')
        $('.category-item.active').removeClass('active')
        $(this).addClass('active')
        $('.category-input').text($(this).text())
        const subcategory = $('.subcategory-filters')
        if (subcategory.hasClass('hidden')) {
            subcategory.removeClass('hidden')
        }
        change_tabs('category', $(this).data('slug'))
    })
    $(document).on('click', '.subcategory-item', function (){
        $('.subcategory-item.active').removeClass('active')
        $(this).addClass('active')
        $('.subcategory-input').text($(this).text())
    })
});