var AWS = require('aws-sdk');
var fs = require('fs');
var s3 = new AWS.S3();
var maxUploadTries = 3;
var bucket = 'coletteandjenpics'
var upload_id = ""
var multipartMap = {
    Parts: []
};


exports.handler = (event, context, callback) => {
    response = upload_to_s3(event,context)
};

function upload_to_s3(data,context){
    binary = data.binary
    part_number = data.part_number
    filename = data.filename
    type = data.type
    done = data.done
    upload_id = data.upload_id
    multipart = data.multipart
    multipartMap = data.multipartMap
    buffer = base64_decode(binary);
    var multiPartParams = {
        Bucket: bucket,
        Key: filename,
        ContentType: type
    };

    if (upload_id.length == 0) {
        s3.createMultipartUpload(multiPartParams, function(mpErr, multipart_data){
          if (mpErr) { console.log('Error!', mpErr); return; }
          console.log("Got upload ID", multipart_data.UploadId);
            partParams = {
              Body: buffer,
              Bucket: bucket,
              Key: filename,
              PartNumber: String(part_number),
              UploadId: multipart_data.UploadId
            };
            upload_id = multipart.UploadId
            uploadPart(s3, multipart_data, partParams,done,0,filename,context);
      });  
    } else {
      partParams = {
        Body: buffer,
        Bucket: bucket,
        Key: filename,
        PartNumber: String(part_number),
        UploadId: upload_id
      };
      uploadPart(s3, multipart, partParams,done,0,filename,context);
    }
  
}

function uploadPart(s3, multipart, partParams,done,tryNum,filename,context) {
  var tryNum = tryNum || 1;
  s3.uploadPart(partParams, function(multiErr, mData) {
    if (multiErr){
      console.log('multiErr, upload part error:', multiErr);
      if (tryNum < maxUploadTries) {
        console.log('Retrying upload of part: #', partParams.PartNumber)
        uploadPart(s3, multipart, partParams, tryNum + 1);
      } else {
        console.log('Failed uploading part: #', partParams.PartNumber)
      }
      return;
    }
    multipartMap.Parts[this.request.params.PartNumber - 1] = {
      ETag: mData.ETag,
      PartNumber: Number(this.request.params.PartNumber)
    };
    console.log("Completed part", this.request.params.PartNumber);
    console.log('mData', mData);
    if (!done) {
      callback(context,{"upload_id":multipart.UploadId,multipart,"multipartMap":multipartMap})
      return; // complete only when all parts uploaded
    } 

    var doneParams = {
      Bucket: bucket,
      Key: filename,
      MultipartUpload: multipartMap,
      UploadId: multipart.UploadId
    };
    console.log(multipartMap)
    console.log("Completing upload...");
    completeMultipartUpload(s3, doneParams);
  });
}

function completeMultipartUpload(s3, doneParams) {
  s3.completeMultipartUpload(doneParams, function(err, data) {
    if (err) {
      console.log("An error occurred while completing the multipart upload");
      console.log(err);
    } else {
      console.log('Final upload data:', data);
    }
  });
}



function base64_decode(base64str, file) {
    var bitmap = new Buffer(base64str, 'base64');
    return bitmap
}

function callback(context,response){
  context.succeed(response)
} 