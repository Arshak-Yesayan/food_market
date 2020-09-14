var like = function(id, what) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            table = JSON.parse(this.response);
            if (table['result']) {
                switch (table['done']) {
                    case 'd_to_l':
                        document.getElementById('dislike_picture_' + id).style.visibility = "visible";
                        document.getElementById('dislike_picture_colored_' + id).style.visibility = "hidden";
                        document.getElementById('like_picture_' + id).style.visibility = "hidden";
                        document.getElementById('like_picture_colored_' + id).style.visibility = "visible";
                        document.getElementById('like_picture_' + id).style.position = "absolute";
                        document.getElementById('like_picture_colored_' + id).style.position = "static";
                        document.getElementById('dislike_picture_' + id).style.position = "static";
                        document.getElementById('dislike_picture_colored_' + id).style.position = "absolute";
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) + 1);
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) - 1);
                        break;
                    case 'l_to_d':
                        document.getElementById('like_picture_' + id).style.visibility = "visible";
                        document.getElementById('like_picture_colored_' + id).style.visibility = "hidden";
                        document.getElementById('dislike_picture_' + id).style.visibility = "hidden";
                        document.getElementById('dislike_picture_colored_' + id).style.visibility = "visible";
                        document.getElementById('dislike_picture_' + id).style.position = "absolute";
                        document.getElementById('dislike_picture_colored_' + id).style.position = "static";
                        document.getElementById('like_picture_' + id).style.position = "static";
                        document.getElementById('like_picture_colored_' + id).style.position = "absolute";
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) - 1);
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) + 1);
                        break;
                    case 'l':
                        document.getElementById('like_picture_' + id).style.visibility = "hidden";
                        document.getElementById('like_picture_colored_' + id).style.visibility = "visible";
                        document.getElementById('like_picture_' + id).style.position = "absolute";
                        document.getElementById('like_picture_colored_' + id).style.position = "static";
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) + 1);
                        break;
                    case 'd':
                        document.getElementById('dislike_picture_' + id).style.visibility = "hidden";
                        document.getElementById('dislike_picture_colored_' + id).style.visibility = "visible";
                        document.getElementById('dislike_picture_' + id).style.position = "absolute";
                        document.getElementById('dislike_picture_colored_' + id).style.position = "static";
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) + 1);
                        break;
                    case 'd_l':
                        document.getElementById('like_picture_' + id).style.visibility = "visible";
                        document.getElementById('like_picture_colored_' + id).style.visibility = "hidden";
                        document.getElementById('like_picture_' + id).style.position = "static";
                        document.getElementById('like_picture_colored_' + id).style.position = "absolute";
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) - 1);
                        break;
                    case 'd_d':
                        document.getElementById('dislike_picture_' + id).style.visibility = "visible";
                        document.getElementById('dislike_picture_colored_' + id).style.visibility = "hidden";
                        document.getElementById('dislike_picture_' + id).style.position = "static";
                        document.getElementById('dislike_picture_colored_' + id).style.position = "absolute";
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) - 1);
                        break;
                }
            }
        }
    }
    xhttp.open("GET", `/products/like?id=${id}&what=${what}`, true);
    xhttp.send();
}