/**
 * Created by didergonzalezarroyave on 5/11/17.
 */
var mongoose = require('mongoose'),
  Schema = mongoose.Schema;

var docsIndexSchema = new Schema({
  _id: String,
  words: [{
    term: String,
    frequency: Number,
    tf_idf: Number
  }]
}, { collection: 'docsIndex' });

var docsModel = mongoose.model('docsIndex', docsIndexSchema);

module.exports = docsModel;
