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
          creator = event.get('creator')
          event_id = event.id
          if @user.get('following').indexOf(creator) > -1
            event_queue = _.clone @user.get('event_queue')
            event_queue.push event_id
            @user.set(event_queue: event_queue)
          if creator == @user.id
            events = _.clone @user.get('events')
            events.push event_id
            @user.set(events: events)
          console.log @user.get("event_queue")
          @navigate '', {trigger: true}

      routes:
        ''                : 'index'
        'login'           : 'login'
        'create'          : 'create'
        'all'             : 'all'
        'user/:user_id'   : 'show_user'
        'event/:event_id' : 'show_event'

      index: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        console.log @user.get("event_queue")
        @fetch_events @user.get("event_queue") if @user.get("logged_in")

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

      all: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        # need to add some sort of pagination here
        $.ajax(
          url: @events.url
          data: {limit: 100000}
        ).done (new_events) =>
          @events.add new_events
          @render_events new_events

      render_events: (events) ->
        events_collection = new Event.collection(events)
        events_view = new EventsView.view(collection: events_collection)
        $('#container').html events_view.render().el

      fetch_events: (event_ids) =>
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

      render_user: (user) ->
        user_view = new UserView.view(model: user)
        $('#user').html user_view.render().el

      show_event: (event_id) ->
        console.log "this should show the event"

      show_user: (user_id) ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        user = if @user.id == user_id then @user else @users.get(user_id)
        if not user?
          user = new User.model(_id: user_id)
          @users.add user
          user.fetch success: =>
            @render_user user
            @fetch_events user.get("events")
        else
          @render_user user
          @fetch_events user.get("events")

    $ ->
      window.router = new Router()
      # Route initial URL
      Backbone.history.start(pushState: true, root: Config.ROOT)

      $(document).foundation()
      UI.initUI()
