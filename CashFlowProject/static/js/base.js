function change_tabs(method, parent_slug){
        console.log(parent_slug)
        $.ajax({
        url: '/change_tabs/',
        type: 'POST',
        data: {
            'method': method,
            'parent_slug': parent_slug
        },
        success: function (data) {
            $('.'+data['response_method']+'-item_container').html(data['html_data'])
        },
    })
}



$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrf_token = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    });
});