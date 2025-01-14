

function save_note(data){
    let edit_type = data['edit_type']

    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: data,
        success: function (data) {
            if (data['success']) {
                $('.save-success').removeClass('hidden')
                if (edit_type === 'delete' || edit_type === 'create') {
                    window.location.href = '/'
                }
            } else {
                $('.save-error').removeClass('hidden')
            }
        },
    })
}


$(document).ready(function () {

    $(document).on('click', '.note-update-button', function (){
        const data = {
            'status': $('.status-item.active').data('slug'),
            'money_type': $('.money_type-item.active').data('slug'),
            'category': $('.category-item.active').data('slug'),
            'subcategory': $('.subcategory-item.active').data('slug'),
            'date_created': $('.date_created-item').val(),
            'money_value': $('.money_value-item').val(),
            'comment': $('.comment-item').val(),
            'edit_type': 'change',
        }
        save_note(data)
    })

    $(document).on('click', '.note-create-button', function (){
        const data = {
            'status': $('.status-item.active').data('slug'),
            'money_type': $('.money_type-item.active').data('slug'),
            'category': $('.category-item.active').data('slug'),
            'subcategory': $('.subcategory-item.active').data('slug'),
            'date_created': $('.date_created-item').val(),
            'money_value': $('.money_value-item').val(),
            'comment': $('.comment-item').val(),
            'edit_type':'create'
        }
        save_note(data)
    })

    $(document).on('click', '.note-delete-button', function (){
        const data = {
            'edit_type': 'delete',
        }
        save_note(data)
    })

    $(document).on('click', '.status-item', function (){
        $('.status-item.active').removeClass('active')
        $(this).addClass('active')
        $('.status-input').text($(this).text())
    })
    $(document).on('click', '.money_type-item', function (){
        $('.money_type-item.active').removeClass('active')
        $(this).addClass('active')
        $('.money_type-input').text($(this).text())

        $('.category-input').text('Категория')
        $('.subcategory-input').text('Подкатегория')
        $('.subcategory-item_container').html('')

        change_tabs('money_type', $(this).data('slug'))
    })
    $(document).on('click', '.category-item', function (){
        $('.category-item.active').removeClass('active')
        $(this).addClass('active')
        $('.category-input').text($(this).text())

        $('.subcategory-input').text('Подкатегория')

        change_tabs('category', $(this).data('slug'))
    })
    $(document).on('click', '.subcategory-item', function (){
        $('.subcategory-item.active').removeClass('active')
        $(this).addClass('active')
        $('.subcategory-input').text($(this).text())
    })
})