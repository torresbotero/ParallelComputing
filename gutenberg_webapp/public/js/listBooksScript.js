/**
 * Created by didergonzalezarroyave on 5/11/17.
 */
$(document).ready(function(){
  var inputWords = document.getElementById('ut').textContent;
  var searchingText = document.getElementById('searchingText');
  var bettersearchingText = document.getElementById('bettersearchingText');
  if(inputWords == ""){
    bettersearchingText.innerHTML = "No words were found in the search field";
    searchingText.innerHTML = "No words were found in the search field";
  }else{
    $.getJSON("/getBooksList/"+inputWords, function(result) {
      if(result.books != ""){
      $("#searchingText").hide();
      $("#bettersearchingText").hide();
        $.each(result.betterBooks, function (i, field) {
          var normal_index = searcharray(field[0],result.books);
          $("#betterContainer").append('<div class="list-group-item list-group-item-action flex-column align-items-start">'
            + '<div class="d-flex w-100 justify-content-between">'
            + '<a href="/search_similarity/' + field[0] + '/' + inputWords + '"><h5 class="mb-1">' + field[0] + ' [Ver relacionados]</h5></a>'
            + '<small class="text-muted">Words found from query: ' + field[1] + '</small><br>'
            + '<small class="text-muted">Total words that match in the document: ' + result.books[normal_index][1] + ' <a target="_blank" href="/gutenberg/' + field[0] + '">[Abrir archivo]</a></small>'
            + '</div>'
            + ' </div>');
        });
          $.each(result.books, function (i, field) {
        var better_index = searcharray(field[0],result.betterBooks);
        if(better_index != undefined){
        /*  $("#betterContainer").append('<div class="list-group-item list-group-item-action flex-column align-items-start">'
            + '<div class="d-flex w-100 justify-content-between">'
            + '<a href="/search_similarity/' + field[0] + '/' + inputWords + '"><h5 class="mb-1">' + field[0] + ' [Ver relacionados]</h5></a>'
            + '<small class="text-muted">Words found from query: ' + result.betterBooks[better_index][1] + '</small><br>'
            + '<small class="text-muted">Total words that match in the document: ' + field[1] + ' <a target="_blank" href="/gutenberg/' + field[0] + '">[Abrir archivo]</a></small>'
            + '</div>'
            + ' </div>'); */
        }else{
          $("#booksContainer").append('<div class="list-group-item list-group-item-action flex-column align-items-start">'
            + '<div class="d-flex w-100 justify-content-between">'
            + '<a href="/search_similarity/' + field[0] + '/' + inputWords + '"><h5 class="mb-1">' + field[0] + ' [Ver relacionados]</h5></a>'
            + '<small class="text-muted">words that match in the document: ' + field[1] + ' <a target="_blank" href="/gutenberg/' + field[0] + '">[Abrir archivo]</a></small>'
            + '</div>'
            + ' </div>');
        }
      });
    }else{
        bettersearchingText.innerHTML = "No results were found";
        searchingText.innerHTML = "No results were found";
      }
    });
  }


});

function sortByKey(array, key) {
  return array.sort(function(a, b) {
    var x = a[key]; var y = b[key];
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  });
}



  function searcharray(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
      if (myArray[i][0] === nameKey) {
        return i;
      }
    }
  }
