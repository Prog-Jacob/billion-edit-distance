'use strict';

var dbm;
var type;
var seed;
var fs = require('fs');
var path = require('path');
var csv = require('csv-parser');
var column_label = "track_name";
/**
  * We receive the dbmigrate dependency from dbmigrate initially.
  * This enables us to not have to rely on NODE_PATH.
  */
exports.setup = function(options, seedLink) {
  dbm = options.dbmigrate;
  type = dbm.dataType;
  seed = seedLink;
};

exports.up = function(db, callback) {
  var results = [];
  var csvPath = path.join(__dirname, '..', 'data', 'train.csv');

  fs.createReadStream(csvPath)
    .pipe(csv())
    .on('data', (row) => {
      results.push(row);
    })
    .on('end', async () => {
      try {
        for (var row of results) {
          await db.insert('songs', [column_label], [row[column_label]]);
        }
        callback();
      } catch (err) {
        callback(err);
      }
    });
};

exports.down = function(db, callback) {
  return db.runSql('DELETE FROM songs;', callback);
};

exports._meta = {
  "version": 1
};