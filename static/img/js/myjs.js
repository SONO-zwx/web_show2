function bigimg(imgid) {
    var modal = document.getElementById('myModal');
    var img = document.getElementById(imgid);
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    img.onclick = function () {
        modal.style.display = "block";
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
    };

    var r = 0;
    $('#zuozhuan').click(function () {
        r -= 90;
        $("#img01").css('transform', 'rotate(' + r + 'deg)');
    });
    $('#youzhuan').click(function () {
        r += 90;
        $("#img01").css('transform', 'rotate(' + r + 'deg)');
    });
    $("#fangda").click(function () {
        var imageWidth = modalImg.width * 1.1;
        var imageHeight = modalImg.height * 1.1;
        $("#img01").css('width', imageWidth + 'px').css('height', imageHeight + 'px');
    });
    $("#suoxiao").click(function () {
        var imageWidth = modalImg.width / 1.1;
        var imageHeight = modalImg.height / 1.1;
        $("#img01").css('width', imageWidth + 'px').css('height', imageHeight + 'px');
    });
}
