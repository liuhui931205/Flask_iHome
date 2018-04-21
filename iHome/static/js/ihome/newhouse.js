function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/v1.0/area',function (resp) {
        if(resp.errno == '0'){
            var areas = resp.data

            var html = template('areas-tmpl',{'areas':areas});

            // for (var i=0;i<areas.length; i++){
            //     var area = areas[i]
            //     $('#area-id').append('<option value="'+ area.aid +'">'+ area.aname +'</option>')
            // }
            $('#area-id').append(html)
        }
        else {
            alert(resp.errmsg)
        }

    });

    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (e) {
        e.preventDefault();

        var house_params = {};
        $(this).serializeArray().map(function (x) {
            house_params[x.name] = x.value

        });
        var facility = [];
        $(':checked[name=facility]').each(function (index,item) {
            facility[index] = item.value
            
        });
        house_params['facility'] = facility;
        
        $.ajax({
            'url':'/api/v1.0/houses',
            'type':'post',
            'data':JSON.stringify(house_params),
            'contentType':'application/json',
            'headers':{
                'X-CSRFToken':getCookie('csrf_token')
                
            },
            'success':function (resp) {
                if (resp.errno == '0'){
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    $('#house-id').val(resp.data.house_id)

                }
                else if(resp.errno == '4101'){
                    location.href = 'login.html'
                }
                else {
                    alert(resp.errmsg)
                }
                
            }
        })

    });

    // TODO: 处理图片表单的数据
        $('#form-house-image').submit(function (e) {
            e.preventDefault()
            $(this).ajaxSubmit({
                'url':'/api/v1.0/houses/image',
                'type':'post',
                'headers':{
                    'X-CSRFToken':getCookie('csrf_token')

                },
                'success':function (resp) {
                    if (resp.errno == '0'){
                        $('.house-image-cons').append('<img src="'+ resp.data.image_url+'">')

                    }
                    else if(resp.errno == '4101'){
                    location.href = 'login.html'
                    }
                    else {
                        alert(resp.errmsg)
                    }

                }
            })

        })

});