require [
  "/static/javascripts/ui.js"
  "/static/javascripts/models/user.js"
  "/static/javascripts/models/event.js"
  "/static/javascripts/views/main_view.js"
  "/static/javascripts/views/side_bar_view.js"
  "/static/javascripts/views/login_view.js"
  "/static/javascripts/views/event_view.js"
  "/static/javascripts/views/events_view.js"
  "/static/javascripts/views/create_view.js"
  "/static/javascripts/views/user_view.js"
  "/static/javascripts/config.js"
  ],
  (UI,
  User,
  Event,
  MainView,
  SideBarView,
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

        if not _.isEmpty(Data.user_to_render)
          user_to_render = new User.model(Data.user_to_render)
          @users.add user_to_render

        if not _.isEmpty(Data.event_to_render)
          event_to_render = new Event.model(Data.event_to_render)
          @events.add event_to_render

        # add event to user's events if the user is the creator
        @events.on 'sync', (event) =>
          creator = event.get('creator')
          event_id = event.id
          if _.contains @user.get('following'), creator
            @user.add_to 'event_queue', event_id
          if creator == @user.id
            @user.add_to 'events', event_id
          @navigate '', {trigger: true}

      routes:
        ''                : 'index'
        'login'           : 'login'
        'create'          : 'create'
        'all'             : 'all'
        'event/:event_id' : 'show_event'
        'user/:user_id'   : 'show_user'
        'search?:q'       : 'search'

      index: ->
        app = new MainView.view(model: @user, columns: [3, 9])
        $('body').html app.render().el

        side_bar = new SideBarView.view()
        $('.column-0').html side_bar.render().el

        $('.column-1').attr('id', 'events')

        @fetch_events @user.get("event_queue") if @user.get("logged_in")

      login: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        login_view = new LoginView.view(model: @user)
        $('.column-0').html login_view.render().el

      create: ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        create_view = new CreateView.view(collection: @events, model: @user)
        $('.column-0').html create_view.render().el

      all: ->
        app = new MainView.view(model: @user, columns: [3, 9])
        $('body').html app.render().el

        side_bar = new SideBarView.view()
        $('.column-0').html side_bar.render().el

        $('.column-1').attr('id', 'events')

        # need to add some sort of pagination here
        $.ajax(
          url: @events.url
          data: {limit: 100000}
        ).done (new_events) =>
          @events.add new_events
          @render_events new_events

      search: (q) ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        # need to add some sort of pagination here
        $.ajax(
          url: @events.url
          data: {q: decodeURIComponent(q)}
        ).done (data) =>
          data = JSON.parse data
          new_events = _.pluck data.results, 'obj'
          @events.add new_events
          @render_events new_events

      render_event: (event) ->
        event_view = new EventView.view(model: event)
        $('#container').html event_view.render().el

      render_events: (events) ->
        events_collection = new Event.collection(events)
        events_view = new EventsView.view(collection: events_collection)
        $('#events').html events_view.render().el

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
        user_view.listenTo(@user, 'change:following', user_view.render)
        $('#user').html user_view.render().el

      show_event: (event_id) ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        event = @events.get(event_id)
        if not event?
          event = new Event.model(_id: event_id)
          @events.add event
          event.fetch success: =>
            @render_event event
        else
          @render_event event


      show_user: (user_id) ->
        app = new MainView.view(model: @user)
        $('body').html app.render().el

        $('.column-0').attr('id', 'user')

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
