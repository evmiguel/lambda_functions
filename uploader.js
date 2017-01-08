var AWS = require('aws-sdk');
var fs = require('fs');
var s3 = new AWS.S3();
var bucket = 'coletteandjenpics'
var done = false


exports.handler = (event, context, callback) => {
    var s3_links = []
    var link_status = {}
    files = event.files
    length = files.length
    for(var i=0; i<length;i++){
        file = files[i]
        filename = file.name
        buffer = base64_decode(file.binary_string)
        var params = {Bucket: 'coletteandjenpics', Key: filename, Body: buffer};
        link_status[filename] = false
        s3.upload(params, function(err, data) {
            s3_links.push(data.Location)
            link_status[data.key] = true
            send_response(link_status,s3_links,callback,length)
        }); 
    }
}

function send_response(statuses,links,callback_func,length){
    status = true
    status_length = 0
    for (var property in statuses) {
        status = (status && statuses[property])
        status_length++
    }
    if(status_length === length && status === true){
        callback_func(null,{"links":links})
    }
}

function base64_decode(base64str,file) {
    var bitmap = new Buffer(base64str, 'base64');
    return bitmap
}

