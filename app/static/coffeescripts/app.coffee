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
    $.fn.serializeObject = ->
      o = {}
      a = @serializeArray()
      $.each a, ->
        if o[@name] != undefined
          if !o[@name].push
            o[@name] = [o[@name]]
          o[@name].push @value or ''
        else
          o[@name] = @value or ''
      return o

    class Router extends Backbone.Router
      initialize: ->
        @user = new User.model(Data.user)
        @users = new User.collection()
        @events = new Event.collection()

        # add event to user's events if the user is the creator
        @events.on 'sync', (event) =>
          if event.get('creator') == @user.id
            events = _.clone @user.get('events')
            events.push event.id
            @user.set('events': events)

      routes:
        ''              : 'index'
        'login'         : 'login'
        'create'        : 'create'
        'user/:user_id' : 'show_user'

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

      render_events: (events) ->
        events_collection = new Event.collection(events)
        events_view = new EventsView.view(collection: events_collection)
        $('#container').html events_view.render().el

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
        if missing_event_ids.length
          $.ajax(
            url: @events.url
            data: {ids: missing_event_ids}
          ).done (new_events) =>
            @events.add new_events
            @render_events events.concat(new_events)
        else
          @render_events events

      show_user: (user_id) ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        user = if @user.id == user_id then @user else @users.get(user_id)
        if not user?
          # fetch current user's events
          user = new User.model(_id: user_id)
          @users.add user
          # render_user and then render_events
          user.fetch(success: @fetch_events)
        else
          @fetch_events user

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: Config.ROOT)

      $(document).foundation()
      UI.initUI()
