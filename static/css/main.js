function showAll() {
    console.log('Clicked!')
    var x = document.getElementById("fullItems");
    var y = document.getElemtnById("goodItems");
    if (x.style.display === "none") {
      x.style.display = "block";
      y.style.display = "none";
    } else {
      x.style.display = "none";
      y.style.display = "block";
    }
  } 