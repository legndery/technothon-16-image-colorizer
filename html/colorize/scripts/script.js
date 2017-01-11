$(document).ready(function(){

    $("#uploadBox").hover(function(){
        $("#backImage").css("filter", "none");
		$("#backImage").css("filter", "grayscale(0%)");
        $("#backImage").css("-webkit-filter", "grayscale(0%)");
    },
    function(){
        $("#backImage").css("filter", "grayscale(100%)");
        $("#backImage").css("-webkit-filter", "grayscale(100%)");
    });

    $("#single-img").hover(function(){
          $("#single-img").css("filter", "grayscale(100%)");
          $("#single-img").css("-webkit-filter", "grayscale(100%)");
        
        $("#backImage").css("filter", "none");
		$("#backImage").css("filter", "grayscale(0%)");
        $("#backImage").css("-webkit-filter", "grayscale(0%)");
        
    },
    function(){
        $("#single-img").css("filter", "none");
        $("#single-img").css("filter", "grayscale(0%)");
        $("#single-img").css("-webkit-filter", "grayscale(0%)");
        
        $("#backImage").css("filter", "grayscale(100%)");
        $("#backImage").css("-webkit-filter", "grayscale(100%)");
        
    });

});
