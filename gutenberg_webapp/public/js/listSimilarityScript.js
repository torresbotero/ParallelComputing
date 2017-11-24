/**
 * Created by didergonzalezarroyave on 6/11/17.
 */
$(document).ready(function(){
  var docName = document.getElementById('docNameSimilarity').textContent;
  var inputWords = document.getElementById('lastinputwords').textContent;
  $.getJSON("/documentsimilarity/"+docName, function(result){
    $.each(result.simil, function(i, field) {
      $("#similContainer").append('<div class="list-group-item list-group-item-action flex-column align-items-start">'
        +'<div class="d-flex w-100 justify-content-between">'
        +'<a href="/search_similarity/' + field[0] + '/' + inputWords + '"><h5 class="mb-1">'+field[0]+' [Ver relacionados]</h5></a>'
        +'<small class="text-muted">Cosine Similarity: '+field[1]+' <a target="_blank" href="/gutenberg/' + field[0] + '">[Abrir archivo]</a></small>'
        +'</div>'
        +' </div>');
    });
  });

});
