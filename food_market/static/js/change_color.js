function change_color(color_from, color_to) {
    table = document.getElementsByClassName('color_changeable');
    for(var i = 0; i < table.length; i++) {
        table[i].style.background = "linear-gradient(180deg, " + color_from + " 0%, " + color_to + " 25%, " + color_to + " 75%, " + color_from + ")";
    }
}

change_color('#20A633', '#0C7F33');