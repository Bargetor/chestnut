function get_wechat_user_info(username, password, callback){
    query_post('/chestnut/support/wechat/user_info/', {'username' : username, 'password' : hex_md5(password)}, get_wechat_user_info_callback);
}

function get_wechat_user_info_callback(data){
    data_json = eval('(' + data + ')');
    document.getElementById("wechat_default_id").value = data_json.wechat_default_id;
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
    // $.ajax({
    //     url : url,
    //     type : "POST",
    //     data : params,
    //     contentType : 'text/json',
    //     dataType : 'text',
    //     success : callback
    // });
    $.post(url, params, callback);
}
