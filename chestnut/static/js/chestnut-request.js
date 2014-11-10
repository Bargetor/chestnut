function get_wechat_user_info(username, password){
    query_get('/chestnut/support/wechat/user_info/', {'username' : username, 'password' : hex_md5(password)}, get_wechat_user_info_callback);
}

function get_wechat_user_info_callback(data){
    alert(data)
}



function query_get(url, params, callback){
    $.ajax({
        url : url,
        type : "GET",
        data : params,
        contentType : 'applicaton/json',
        dataType : 'text',
        success : callback
    });
}

function query_post(url, params, callback){
    $.ajax({
        url : url,
        type : "POST",
        data : params,
        contentType : 'text/xml',
        dataType : 'text',
        success : callback
    });
    // $.post(url, params, callback);
}
