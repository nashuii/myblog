/**
 * Created by J on 2017/11/20.
 */

// 初始化simditor的函数
$(function() {
	var editor,toolbar;
	toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale', 'color', '|', 'code', '|', 'link', 'image', 'hr', '|', 'alignment'];
	Simditor.locale = 'zh-CN';
	editor = new Simditor({
		textarea: $('#simditor'),
		toolbar: toolbar,
		pasteImage: true
	});
	// 加到window上去,其他地方才能访问到editor这个变量
	window.editor = editor;
});

$(function(){
    $('#commit-btn').click(function(){
        var text = editor.getValue();
        var article_uid = window.location.href.match(/article_uid=(\S+)/)[1];
        var data = {
            'text':text,
            'article_uid':article_uid
        };
        myajax.post({
            'url':'/cms/discuss/',
            'data':data,
            'success':function(result){
                if(result['code'] == 200){
                    var data = result['data'];
                    var dis_tp = template('cms_discuss_template',{'avatar':data['avatar'],'auth':data['auth'],'text':text});
                    $('#discuss-content').append(dis_tp);
                }else{
                    console.log(result['message']);
                }
            },
            'error':function(error){
                console.log(error);
            }
        });
    });
});