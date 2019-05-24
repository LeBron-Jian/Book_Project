// 从cookie取 csrf token 的值
function getCookie(name){
    var cookieValue = null;
    if (document.cookie && document.cookie !== ''){
        var cookies = document.cookie.split(';');
        for (var i =0; i<cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie srting begin with the name we want?
            if (cookies.substring(0, name.length +1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length +1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// 将csrftoken 设置到ajax 请求头中，后续的ajax请求就会自动携带这个 csrf token
function csrfSafeMethod(method) {
    // these HTTP  methods do not require  CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend:function (xhr, settings) {
        if (! csrfSafeMethod(settings.type) && !this.crossDomain){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});