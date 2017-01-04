var AWS = require('aws-sdk');
var fs = require('fs');
var s3 = new AWS.S3();
var bucket = 'coletteandjenpics'


exports.handler = (event, context, callback) => {
    files = event.files
    console.log(files)
    for(var i=0; i< files.length; i++){
        file = files[i]
        buffer = base64_decode(file.binary_string)
        var params = {Bucket: 'coletteandjenpics', Key: file.name, Body: buffer};
        s3.upload(params, function(err, data) {
            console.log(data)
        });
    }
};



function base64_decode(base64str,file) {
    var bitmap = new Buffer(base64str, 'base64');
    return bitmap
}

