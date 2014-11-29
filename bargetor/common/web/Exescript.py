# -*- coding:utf-8 -*-
#
# created by heqingpan

_init_js="""
(function (){
    if (window.__e){
        return;
    }
    var e=document.createElement('div');
    e.setAttribute("id","__s_msg");
    e.style.display="none";
    document.body.appendChild(e);
    window.__e=e;
})();

window.__s_set_msg = function(a){
    if(typeof a == 'object' && a != null){
        window.__e.setAttribute("msg", json2str(a) || "");
    }else if(a != null){
        window.__e.setAttribute("msg", a.toString() || "");
    }else{
        window.__e.setAttribute("msg", "");
    }
}

function json2str(o) {
    var arr = [];
    var fmt = function(s) {
    if (typeof s == 'object' && s != null) return json2str(s);
        return /^(string|number)$/.test(typeof s) ? '"' + s + '"' : s;
    }
    for (var i in o) arr.push('"' + i + '":' + fmt(o[i]));
    return '{' + arr.join(',') + '}';
}
"""
_loadJsFmt="""
var script = document.createElement('script');
script.src = "{0}";
document.body.appendChild(script);
"""
_jquery_cdn = "http://lib.sinaapp.com/js/jquery/1.7.2/jquery.min.js"
_warp_js_fmt = "__s_set_msg((function(){%s})())"

class ExeJs(object):
    def __init__(self, driver, trytimes=10):
        from time import sleep
        self.driver = driver
        driver.execute_script(_init_js)
        while trytimes > 0:
            try:
                self.msgNode = driver.find_element_by_id('__s_msg')
                break
            except Exception:
                sleep(1)
                trytimes -= 1
        if self.msgNode is None:
            raise Exception()

    def exeWrap(self, js_str):
        """ jsstr 执行后有返回值，返回值通过self.getMsg()获取 """
        _warp_js_fmt_temp = _warp_js_fmt
        js = _warp_js_fmt_temp % (js_str)
        self.driver.execute_script(js)

    def loadJs(self, path):
        self.execute(_loadJsFmt.format(path))

    def loadJquery(self, path=_jquery_cdn):
        self.loadJs(path)

    def execute(self, js_str):
        self.driver.execute_script(js_str)

    def getMsg(self):
        return self.msgNode.get_attribute('msg')
