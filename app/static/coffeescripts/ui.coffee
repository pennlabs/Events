define [], ->
  return {
    initUI: ->
      $(".sidebar-fold").click ->
        $(".sidebar").toggleClass("folded")
        
      $(window).scroll ->
        if window.pageYOffset > $(".top-bar").height()
          $(".sidebar").addClass("stick")
        else
          $(".sidebar").removeClass("stick")
  }
