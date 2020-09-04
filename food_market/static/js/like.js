var like = function(id, what) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            table = JSON.parse(this.response);
            if (table['result']) {
                if (what == 'like') {
                    likes = document.getElementById("likes_" + id).textContent;
                    console.log(likes);
                    document.getElementById("likes_" + id).innerHTML = String(parseInt(document.getElementById("likes_" + id).textContent) + 1);
                }
                else if (what == 'dislike') {
                    dislikes = document.getElementById("dislikes_" + id).textContent;
                    console.log(dislikes);
                    document.getElementById("dislikes_" + id).innerHTML = String(parseInt(document.getElementById("dislikes_" + id).textContent) + 1);
                }
            }
        }
    }
    xhttp.open("GET", "/products/like?id=" + id + '&what=' + what, true);
    xhttp.send();
}