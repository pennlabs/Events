define ['static/scripts/vendor/text!static/scripts/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events:
        'click a.home'  : 'index'
        'click a.login' : 'login'
      index: (e) ->
        e.preventDefault()
        window.router.navigate '', {trigger: true}
      login: (e) ->
        e.preventDefault()
        window.router.navigate 'login', {trigger: true}
      render: ->
        @$el.html template
        return @

    return {view: MainView}
