/**
 * Created by didergonzalezarroyave on 6/11/17.
 */
var mongoose = require('mongoose'),
  Schema = mongoose.Schema;

var cosineSimilaritySchema = new Schema({
  _id: String,
  simil_docs: [{
    doc_name: String,
    similarity: Number
  }]
}, { collection: 'cosineSimilarity' });

var docsModel = mongoose.model('cosineSimilarity', cosineSimilaritySchema);

module.exports = docsModel;
