/**
 * Created by J on 2017/10/19.
 */

'use strict';

$(document).ready(function(){
    var current_url = window.location.href;
    var current_index = 0;
    if(current_url.indexOf('add_article') > 0){
        current_index = 1;
    }else if(current_url.indexOf('news') > 0){
        current_index = 2;
    }else if(current_url.indexOf('settings') > 0){
        current_index = -1;
    }else{
        current_index = 0;
    }
    var ultag = $(".menu-ul");
    if(current_index >=0 ){
        ultag.children().eq(current_index).addClass('active').siblings().removeClass('active');
    }else{
        ultag.children().siblings().removeClass('active');
    }
});