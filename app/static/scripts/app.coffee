require [
  'static/scripts/models/user',
  'static/scripts/views/main_view',
  'static/scripts/views/login_view',
  ],
  (User, MainView, LoginView) ->
    # push window.user into the Router class
    class Router extends Backbone.Router
      initialize: ->
        @user = new User.model(Data.user)
      routes:
        ''          : 'index'
        'login'     : 'login'
      index: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el
        # fetch events and render them
        # render sidebar

      login: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        login_view = new LoginView.view(model: @user)
        $('#container').html login_view.render().el

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: '/events')
