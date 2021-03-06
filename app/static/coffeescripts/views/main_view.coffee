define ['/static/javascripts/vendor/text.js!/static/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events:
        'click a.home'            : 'index'
        'click a.login'           : 'login'
        'click a.logout'          : 'logout'
        'click .card .title'      : 'event'
        'click a.create'          : 'create'
        'click a.user'            : 'user'
        'click a#search'          : 'search'
        'submit form.search'      : 'search'
      initialize: (options) ->
        @columns = options.columns or [12]
      index: (e) ->
        e.preventDefault()
        window.router.navigate '', {trigger: true}
      login: (e) ->
        e.preventDefault()
        window.router.navigate 'login', {trigger: true}
      logout: (e) ->
        e.preventDefault()
        @model.logout()

        # See: https://github.com/documentcloud/backbone/issues/652#issuecomment-10731041
        if Backbone.history.fragment == ''
          Backbone.history.loadUrl Backbone.history.fragment
        else
          router.navigate '', {'trigger': true}
      create: (e) ->
        e.preventDefault()
        window.router.navigate 'create', {trigger: true}

      event: (e) ->
        e.preventDefault()
        window.router.navigate 'event', {trigger: true}

      user: (e) ->
        e.preventDefault()
        window.router.navigate "user/#{@model.id}", {trigger: true}

      render: ->
        compiled = _.template template, _.extend(@model.toJSON(), columns: @columns)
        @$el.html compiled
        return @

      search: (e) ->
        e.preventDefault()
        q = $('#searchbox').val()
        window.router.navigate "search?q=#{encodeURIComponent(q)}", {trigger: true}

    return {view: MainView}
