$(".login_btn").on("click", function () {

    $.ajax({
        url: "",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            user: $("#user").val(),
            pwd: $("#pwd").val(),
            valid_code: $("#valid_code").val(),
        },
        success: function (data) {
            console.log(data)
            if (data.state) {
                location.href = "/index/"
            }
            else {
                $(".error").text(data.msg)
            }

        }
    })

})
$("#code_img").on("click",function () {
    $(this)[0].src+="?";
})