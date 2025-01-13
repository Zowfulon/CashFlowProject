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

function change_tabs(method, parent_slug){
        $.ajax({
        url: '/change_tabs/',
        type: 'POST',
        data: data,
        success: function (data) {
            if (method === 'money_type'){

            } else {

            }
        },
    })
}


$(document).ready(function () {


    $('.note-filter-button').click(function (){
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
    $('.money_type-item').click(function (){
        $('.money_type-item.active').removeClass('active')
        $(this).addClass('active')
        const subcategory = $('.subcategory-filters')
        if (!subcategory.hasClass('hidden')){
            subcategory.addClass('hidden')
        }
        const category = $('.category-filters')
        if (category.hasClass('hidden')) {
            category.removeClass('hidden')
        }
    })
    $('.category-item').click(function (){
        $('.category-item.active').removeClass('active')
        $(this).addClass('active')
        const subcategory = $('.category-filters')
        if (subcategory.hasClass('hidden')) {
            subcategory.removeClass('hidden')
        }
    })
    $('.subcategory-item').click(function (){
        $('.subcategory-item.active').removeClass('active')
        $(this).addClass('active')
    })
});