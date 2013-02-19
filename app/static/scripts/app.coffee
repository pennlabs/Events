require [
  'static/scripts/views/main_view',
  'static/scripts/views/login_view',
  ],
  (MainView, LoginView) ->
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
        app = new LoginView.view()
        $('body').html app.render().el
        console.log "login"

      show_event: (event_id) ->
        event = @collection.get(event_id)

    $ ->
      router = new Router()

      # Route initial URL
      Backbone.history.start(pushState: true)
