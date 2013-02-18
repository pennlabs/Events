require ['static/scripts/views/main_view'],
  (MainView) ->
    $ ->
      app = new MainView.view()
      $('body').html app.render().el
