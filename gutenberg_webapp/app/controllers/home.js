const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const InvertedIndex = mongoose.model('InvertedIndex');
const docsIndex = mongoose.model('docsIndex');
const cosineSimilarity = mongoose.model('cosineSimilarity');
var forEach = require('async-foreach').forEach;
var dict = require("dict");

module.exports = function (app) {
  app.use('/', router);
};



router.get('/', function(req, res, next){
  res.render('index', {
    title: 'Gutenberg Documents Search and Similarity Detection'
  });
});



router.post('/search_text', (req, res, next) => {
  var text_to_search = req.body.textInput
  if(text_to_search.trim() != ""){
    var searched_words = (text_to_search).trim().split(' ')
    res.render('results', {
      title: 'Results of the search',
      searched: ''+searched_words,
      search_response: text_to_search
    });
  }else{
    res.render('results', {
    title: 'Results of the search',
    searched: "",
    search_response: ""
  });
  }
});


router.get('/backto_search/:last_search', (req, res, next) => {
  var last_search = req.params.last_search
  var searched_words = (last_search).trim().split(' ')
  res.render('results', {
  title: 'Results of the search',
  searched: ''+searched_words,
  search_response: last_search
});
});


router.get('/search_similarity/:document_name/:lastinput_words', (req, res, next) => {
  var doc_name = req.params.document_name
  var lastinput_words = req.params.lastinput_words
  res.render('Similarity', {
    title: '10 Most similar documents',
    searched: doc_name,
    lastinputwords: lastinput_words
  });
});



router.get('/getBooksList/:inputText', function(req, res) {

  try {
    var inputText = req.params.inputText;
  } catch (ex) {
    console.log('failed');
    return;
  }

  var text_to_search = (inputText).trim().split(' ')
  var itemsProcessed = 0;
  var alldocuments = dict({});
  var betterdocuments = dict({});
  forEach(text_to_search, function(item, index, arr) {
    docsIndex.find({"words.term":item},{ _id: 1, 'words':{'$elemMatch': {'term':item}}, "words.term":1, "words.frequency":1},function(err, indexes){
      foundDocuments = 0;
      forEach(indexes, function(doc, index, arr) {
       /* if(doc["_id"] == "2000-8.txt"){
          console.log(item)
          console.log("uno")
        } */
        if(betterdocuments.has(doc["_id"])){

          if(betterdocuments.get(doc["_id"]) < (itemsProcessed+1)){
            betterdocuments.set(doc["_id"], (betterdocuments.get(doc["_id"])+1));
          }
        }else{
          betterdocuments.set(doc["_id"], 1);
        }
        if(alldocuments.has(doc["_id"])){
          alldocuments.set(doc["_id"], (alldocuments.get(doc["_id"]) + doc["words"][0]["frequency"]));
        }else{
          alldocuments.set(doc["_id"], doc["words"][0]["frequency"]);
        }
        foundDocuments++;
      });



      itemsProcessed++;
 // console.log(itemsProcessed)
    //  console.log(text_to_search.length)
      if((itemsProcessed === text_to_search.length) && (foundDocuments === indexes.length)) {
        //console.log('2000-8.txt: '+betterdocuments.get("2000-8.txt"))
        allDone(alldocuments,betterdocuments);
      }
    });
  });

  function allDone(d,better_d) {
    if(d.size != 0) {
      var result = {}
      var betterResult = {}
      var itemsSecondProcessed = 0;
      var betterSecondProcessed = 0;
    better_d.forEach(function (value, key) {
      if(value > 1){
        betterResult[key]=value;
      }
      betterSecondProcessed++;
      if (betterSecondProcessed === better_d.size) {
        d.forEach(function (value, key) {
         /* if(betterResult[key] == undefined){

          }*/
          result[key] = value;
          itemsSecondProcessed++;
          if (itemsSecondProcessed === d.size) {
            res.send({'books': sortProperties(result), 'betterBooks':sortProperties(betterResult)})
          }
        });
      }
      });


    }else{
      res.send({'books': ""})
    }
  }

});



router.get('/documentsimilarity/:document_name', function(req, res) {
  var doc_name = req.params.document_name

  cosineSimilarity.find({_id:doc_name},{_id: 0,"simil_docs.doc_name":1, "simil_docs.similarity":1},function (err,books) {
    if(err){
      console.log("No fue posible obtener el detalle del libro con id: "+req.params.document_name);
      return;
    }
    if(books != null && books != undefined){
      similar_docs = books[0]["simil_docs"]
      var similarProcessed = 0;
      var result = {}
      forEach(similar_docs, function(item, index, arr) {
        if(item["doc_name"] != doc_name){
          result[item["doc_name"]] = item["similarity"];
        }
        similarProcessed++;
        if(similarProcessed === similar_docs.length) {
          res.send({'simil' : sortProperties(result).slice(0, 10)})
        }
      })

    }
  })
});


function sortProperties(obj)
{
  // convert object into array
  var sortable=[];
  for(var key in obj)
    if(obj.hasOwnProperty(key))
      sortable.push([key, obj[key]]); // each item is an array in format [key, value]

  // sort items by value
  sortable.sort(function(a, b)
  {
    return b[1]-a[1]; // compare numbers
  });
  return sortable; // array in format [ [ key1, val1 ], [ key2, val2 ], ... ]
}
