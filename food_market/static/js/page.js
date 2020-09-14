var pages = document.getElementById('pages');
var search = location.search.substring(1);
var got_arr = {};

if(decodeURI(search) != '') {
    var got_arr = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
}

for(var i = 0; i < pages.children.length; i++) {
    var page = pages.children[i].firstChild;
    var params = `name=${got_arr['name']}&category=${got_arr['category']}&p_from=${got_arr['p_from']}&p_to=${got_arr['p_to']}&sort=${got_arr['sort']}&`;
    page.href = `/products?${params}page=${page.textContent}`;
}