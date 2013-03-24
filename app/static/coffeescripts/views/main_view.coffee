define ['static/javascripts/vendor/text!static/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events:
        'click a.home'      : 'index'
        'click a.login'     : 'login'
        'click a.logout'    : 'logout'
        'click .card .title'  : 'event'
        'click a.create'    : 'create'
        'click a.user'      : 'user'
        'click .card .subtitle a'      : 'user'
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
        window.router.navigate 'user', {trigger: true}

      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: MainView}