(function($){$.fn.extend({getCurPos:function(){var curCurPos='';var all_range='';if(navigator.userAgent.indexOf("MSIE")>-1){if($(this).get(0).tagName=="TEXTAREA"){all_range=document.body.createTextRange();all_range.moveToElementText($(this).get(0));}else{all_range=$(this).get(0).createTextRange();}
$(this).focus();var cur_range=document.selection.createRange();cur_range.moveEnd('character',-cur_range.text.length)
cur_range.setEndPoint("StartToStart",all_range);curCurPos=cur_range.text.length;}else{$(this).focus();curCurPos=$(this).get(0).selectionStart;}
return curCurPos;},setCurPos:function(start,end){if(navigator.userAgent.indexOf("MSIE")>-1){var all_range='';if($(this).get(0).tagName=="TEXTAREA"){all_range=document.body.createTextRange();all_range.moveToElementText($(this).get(0));}else{all_range=$(this).get(0).createTextRange();}
$(this).focus();all_range.moveStart('character',start);all_range.moveEnd('character',-(all_range.text.length-(end-start)));all_range.select();}else{$(this).focus();$(this).get(0).setSelectionRange(start,end);}},});})(jQuery);