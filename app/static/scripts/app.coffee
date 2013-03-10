require [
  'static/scripts/models/user',
  'static/scripts/views/main_view',
  'static/scripts/views/login_view',
  'static/scripts/views/event_view',
  'static/scripts/config'
  ],
  (User,
  MainView,
  LoginView,
  EventView,
  Config) ->
    class Router extends Backbone.Router
      initialize: ->
        @user = new User.model(Data.user)

      routes:
        ''          : 'index'
        'login'     : 'login'
        'event'     : 'event'

      index: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

      login: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        login_view = new LoginView.view(model: @user)
        $('#container').html login_view.render().el

      event: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        @event = null

        view = new EventView.view()
        $('#container').html view.render().el

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: Config.ROOT)
      $(document).foundation()
