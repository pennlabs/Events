require [
  'static/scripts/models/user',
  'static/scripts/views/main_view',
  'static/scripts/views/login_view',
  ],
  (User, MainView, LoginView) ->
    window.user = null
    class Router extends Backbone.Router
      routes:
        ''          : 'index'
        'login'     : 'login'
        'event/:id' : 'show_event'
      index: ->
        window.user ||= new User.model()
        app = new MainView.view(model: window.user)
        $('body').html app.render().el
        # fetch events and render them
        # render sidebar

      login: ->
        window.user ||= new User.model()
        app = new MainView.view(model: window.user)
        $('body').html app.render().el

        login_view = new LoginView.view(model: window.user)
        $('#container').html login_view.render().el

      show_event: (event_id) ->
        event = @collection.get(event_id)

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: '/')
