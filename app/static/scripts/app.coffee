require ['static/scripts/views/main_view'],
  (MainView) ->
    class Router extends Backbone.Router
      routes:
        ''          : 'index'
        'login'     : 'login'
        'event/:id' : 'show_event'

      index: ->
        app = new MainView.view()
        $('body').html app.render().el
        # fetch events and render them
        # render sidebar

      login: ->
        app = new MainView.view()
        $('body').html app.render().el

      show_event: (event_id) ->
        event = @collection.get(event_id)

    $ ->
      router = new Router()
      Backbone.history.start(pushState: true)
