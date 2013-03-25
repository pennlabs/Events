require [
  "/static/javascripts/ui.js"
  "/static/javascripts/models/user.js"
  "/static/javascripts/models/event.js"
  "/static/javascripts/views/main_view.js"
  "/static/javascripts/views/login_view.js"
  "/static/javascripts/views/event_view.js"
  "/static/javascripts/views/events_view.js"
  "/static/javascripts/views/create_view.js"
  "/static/javascripts/views/user_view.js"
  "/static/javascripts/config.js"
  ],
  (
  UI,
  User,
  Event,
  MainView,
  LoginView,
  EventView,
  EventsView,
  CreateView,
  UserView,
  Config) ->
    class Router extends Backbone.Router
      initialize: ->
        @user = new User.model(Data.user)
        @users = new User.collection()
        @events = new Event.collection()

      routes:
        ''                   : 'index'
        'login'              : 'login'
        'create'             : 'create'
        'user/:user_id'      : 'show_user'

      index: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

      login: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        login_view = new LoginView.view(model: @user)
        $('#container').html login_view.render().el

      create: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        create_view = new CreateView.view(collection: @events, model: @user)
        $('#container').html create_view.render().el

      fetch_events: (user) =>
        event_ids = user.get("events")
        events = []
        missing_event_ids = []
        for event_id in event_ids
          event = @events.get(event_id)
          # add event id to missing event ids
          if not event?
            missing_event_ids.push event_id
          else
            events.push event
        $.ajax(
          url: @events.url
          data: {ids: missing_event_ids}
        ).done (new_events) =>
          @events.add new_events
          events = new Event.collection(events.concat new_events)
          events_view = new EventsView.view(collection: events)
          $('#container').html events_view.render().el


      show_user: (user_id) ->
        user = if @user.id == user_id then @user else @users.get(user_id)
        if not user?
          # fetch current user's events
          user = new User.model("_id": user_id)
          @users.add user
          user.fetch(success: @fetch_events)
        else
          @fetch_events(user)

        app = new MainView.view(model: @user)
        $('body').html app.render().el

        # user_view = new UserView.view(model: @user)
        # $('#container').html user_view.render().el

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: Config.ROOT)

      $(document).foundation()
      UI.initUI()
