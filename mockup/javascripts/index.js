$(function() {
  
  $(".sidebar-fold").click(function(){
    $(".sidebar").toggleClass("folded");
  })
  
  $(window).scroll(function() {
    if (window.pageYOffset > $(".top-bar").height())
      $(".sidebar").addClass("stick");
    else
      $(".sidebar").removeClass("stick");
  });
  
});