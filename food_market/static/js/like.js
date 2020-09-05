var like = function(id, what) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            table = JSON.parse(this.response);
            if (table['result']) {
                switch (table['done']) {
                    case 'd_to_l':
                        likes = document.getElementById("likes_" + id).textContent;
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) + 1);
                        dislikes = document.getElementById("dislikes_" + id).textContent;
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) - 1);
                        break;
                    case 'l_to_d':
                        likes = document.getElementById("likes_" + id).textContent;
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) - 1);
                        dislikes = document.getElementById("dislikes_" + id).textContent;
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) + 1);
                        break;
                    case 'l':
                        likes = document.getElementById("likes_" + id).textContent;
                        document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) + 1);
                        break;
                    case 'd':
                        dislikes = document.getElementById("dislikes_" + id).textContent;
                        document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) + 1);
                        break;
                }
            }
        }
    }
    xhttp.open("GET", "/products/like?id=" + id + '&what=' + what, true);
    xhttp.send();
}