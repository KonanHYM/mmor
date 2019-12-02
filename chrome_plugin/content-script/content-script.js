(function() {
	alert("注入成功");
	chrome.runtime.onMessage.addListener(
		alert("注入成功");
    	function (request, sender, sendResponse) {
        	if (request.action == "send") {
            	sendResponse({state:'关键词填写成功！'});
				alert("关键词填写成功！");
        	}
    	}
	);
})();
