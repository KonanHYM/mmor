$(function(){
    $('#b2b_vcp_parser').click(function () {//给对象绑定事件
        console.log("log");
        chrome.tabs.query({active:true, currentWindow:true}, function (tab) {//获取当前tab
        //向tab发送请求
        chrome.tabs.sendMessage(tab[0].id, {
            action: "send",
            keyword: $('#inputGroupSelect04').val()
        }, function (response) {
            console.log(response);
            });
        });
    });
})
