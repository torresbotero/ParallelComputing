const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const InvertedIndexSchema = new Schema({
  _id: String,
  docs: [{
    doc_name: String
  }]
}, { collection: 'invertedIndex' });

mongoose.model('InvertedIndex', InvertedIndexSchema);

