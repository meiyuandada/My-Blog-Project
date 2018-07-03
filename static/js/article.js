$(".btn-db").click(function () {
    var username = $("#info").attr("username");
    if (username) {
        //确定当前点击的是哪个按钮 是点赞还是反对
        var is_up = $(this).hasClass("diggit");
        console.log('-----', $(this))
        //拿到当前文章的对应id
        var article_id = $("#info").attr("article_id");

        $.ajax({
            url: "/blog/poll/",
            type: "POST",
            data: {
                is_up: is_up,
                article_id: article_id,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                console.log('11111', data);
                // 如果状态是True那么就添加减少计数
                if (data.state) {
                    if (is_up) {
                        var val = parseInt($("#diggit_count").text()) + 1;
                        $("#diggit_count").text(val)
                    } else {
                        var val = parseInt($("#buryit_count").text()) + 1;
                        $("#buryit_count").text(val)
                    }
                } else {  // 否则就提示不能重复操作哦
                    console.log('22222', data.first_operate);
                    if (data.first_operate) {// 点赞了就提示点赞了
                        $("#digg_word").stop(true, false).slideDown(1000);
                        $("#digg_word").text("您已经推荐过");
                        $("#digg_word").slideUp(3000);
                    } else {
                        $("#digg_word").stop(true, false).slideDown(1000);
                        $("#digg_word").text("您已经反对过");
                        $("#digg_word").slideUp(3000);
                    }
                }
            }
        })

    } else {
        location.href = "/login/"
    }
})

//////////////////////////////////////////////////////////////////////////

var pid = ""; //pid全局变量
$(".comment_btn").click(function () {
    //拿到html静态存储到属性里的username
    var username = $("#info").attr("username");


    //如果登陆的话
    if (username) {
        //拿到html静态存储到属性里的aritcle_id
        var article_id = $("#info").attr("article_id");

        var $c_val = $.trim($("#comment_text").val());
        if ($c_val) {

            if ($("#comment_text").val()[0]!=="@"){
                pid = '';
            }
            //如果是对根评论回复的话 截取评论内容
            if (pid) {
                var index = $("#comment_text").val().indexOf("\n");
                var content = $("#comment_text").val().slice(index + 1);
            } else {
                var content = $("#comment_text").val()
            }

            $.ajax({
                url: "/blog/comment/",
                type: "post",
                data: {
                    article_id: article_id,
                    content: content,
                    pid: pid,
                    csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                }, success: function (data) {
                    console.log(data);
                    if (data.state) {
                        alert("------------->start")
                        $("#comment_text").val("");
                        alert("--------->")
                        pid = "";
                        location.reload();
                    } else {
                        alert("state is wrong");
                    }
                }
            })
        }else {
            alert("评论内容不能为空哦！")
        }
    } else {
        location.href = "/login/"
    }

});

//////////////////////////////////////////////////////////////////////////

//对回复按钮绑定事件
$(".reply").click(function () {

    $("#comment_text").focus();
    var val = "@" + $(this).attr("username") + "\n";
    $("#comment_text").val(val)

    pid = $(this).attr("pk")

})