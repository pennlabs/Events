define ['static/scripts/vendor/text!static/scripts/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events:
        'click a.login' : 'login'
      login: (e) ->
        e.preventDefault()
        window.router.navigate 'login', {trigger: true}
      render: ->
        @$el.html template
        return @

    return {view: MainView}
