$(document).ready(function(){
$('.babody').hide();
	$('#loadingAnim').hide();
	$('.output-sub-div').hide();
  $('#uploadForm').submit(function (event){

	  $('html, body').animate({
        scrollTop: $("#output-div").offset().top
    	}, 2000);
		$('.output-sub-div').hide();
    $('#loadingAnim').show();

    event.preventDefault();
    var fd = new FormData();

		var mfile = $('input[type="file"]')[0].files[0];
    if (mfile) {
      fd.append('file', mfile);
    }

    //fd.append("file", blobFile);
      console.log("typeof fd-n "+typeof fd);
    $.ajax({
      url: "/fl/upload",
      type: "POST",
      data: fd,
      processData: false,
      contentType: false,
      success: function(response) {
        $('.babody').show("slow");
        $('#loadingAnim').hide();
        //alert("response"+response.result.color);
        var res = response.result;
		  console.log("response"+res);
        //var img=res.color.files[0].size;
        var wd=response.Width;
        var ht=response.Height;
        var beforeD=$('.subject-before');
        var afterD=$('.subject-after');
				var singleImg=$('#single-img');
				var sImgLink=$('#output-img-link');
				var outImgLink=$('#output-page-img');
        /*
        if(ht>600){
            beforeD.height(ht/2);
            beforeD.width(wd/2);

            afterD.height(ht/2);
            afterD.width(wd/2);
          }
          */
          console.log("width:"+wd + ", height:"+ht);
        //beforeD.attr("src",res.color);
				singleImg.attr("src",res.color);
				sImgLink.attr("href",res.color);
				outImgLink.attr("href",res.color);
				outImgLink.attr("src",res.color);

        //afterD.attr("src",res.color);
        console.log(response);
				$('.output-sub-div').show();
      },
      error: function(jqXHR, textStatus, errorMessage) {
        console.log(errorMessage); // Optional
      }
    });
  });
});
