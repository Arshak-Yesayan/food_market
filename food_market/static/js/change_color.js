var colors = document.getElementsByClassName('color_changeable');
var p_hide = document.getElementById('hide_color');
var color_control = document.getElementById('color_change');
var colorings = [['#20A633', '#0C7F33'], ['#2E8DDC', '#064F8C']];
var hiden = false;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function change_color(name) {
    for(var i = 0; i < colors.length; i++) {
        colors[i].style.background = `linear-gradient(180deg, ${colorings[name][0]} 0%, ${colorings[name][1]} 25%, ${colorings[name][1]} 75%, ${colorings[name][0]})`;
    }
}

function hide() {
    if( hiden ) {
        hiden = false;
        p_hide.innerHTML = '»';
        color_control.style.right = "0px";
    }
    else {
        hiden = true;
        p_hide.innerHTML = '«';
        color_control.style.right = "-110px";
    }
}

change_color(0);

for(var x = 0; x < color_control.children.length; x++) {
    color_control.children[x].style.background = `linear-gradient(180deg, ${colorings[x][1]} 0%, ${colorings[x][0]} 25%, ${colorings[x][0]} 75%, ${colorings[x][1]})`;
}