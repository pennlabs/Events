requirejs.onError = (err) ->
  if err.requireType == 'scripterror'
    alert "please copy static/scripts/config.coffee.default!"
  throw err

require [
  "static/javascripts/ui"
  "static/javascripts/models/user"
  "static/javascripts/views/main_view"
  "static/javascripts/views/login_view"
  "static/javascripts/views/event_view"
  "static/javascripts/views/create_view"
  "static/javascripts/views/user_view"
  "static/javascripts/config"
  ],
  (
  UI,
  User,
  MainView,
  LoginView,
  EventView,
  CreateView,
  UserView,
  Config) ->
    class Router extends Backbone.Router
      initialize: ->
        @user = new User.model(Data.user)
        @events = new Events.collection()

      routes:
        ''          : 'index'
        'login'     : 'login'
        'event'     : 'event'
        'create'    : 'create'
        'user'      : 'user'

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
        
      create: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        create_view = new CreateView.view(model: @user)
        $('#container').html create_view.render().el
      
      user: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        user_view = new UserView.view(model: @user)
        $('#container').html user_view.render().el

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: Config.ROOT)
      
      $(document).foundation()
      UI.initUI()
