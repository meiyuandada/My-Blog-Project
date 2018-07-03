// 图像预览

$("#avatar").change(function () {
    var choose_file = $(this)[0].files[0];
    var reader = new FileReader();
    reader.readAsDataURL(choose_file);
    reader.onload = function () {
        $(".avatar").attr("src", reader.result)
    }
})


// 注册事件
$(".reg_btn").click(function () {
    var formdata = new FormData();
    formdata.append("user", $("#id_user").val());
    formdata.append("pwd", $("#id_pwd").val());
    formdata.append("repeat_pwd", $("#id_repeat_pwd").val());
    formdata.append("email", $("#id_email").val());
    formdata.append("avatar", $("#avatar")[0].files[0]);
    formdata.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());

    $.ajax({
        url: "",
        type: "post",
        processData: false,
        contentType: false,
        data: formdata,
        success: function (data) {
            //console.log(data)
            if (data.user) {
                // 注册成功
                location.href = "/login/"
            } else {
                console.log(data.error_dict);
                // q清空错误信息
                $("form span").html("");
                $("form .form-group").removeClass("has-error")
                // 加载错误信息
                $.each(data.error_dict, function (field, error_list) {

                    if (field == "__all__") {
                        $("#id_repeat_pwd").next().html(error_list[0]).css("color", 'red');
                        $("#id_repeat_pwd").parent().addClass("has-error")
                    }

                    $("#id_" + field).next().html(error_list[0]).css("color", 'red');
                    $("#id_" + field).parent().addClass("has-error")
                })
            }
        }
    })
})