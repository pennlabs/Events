define ['static/scripts/vendor/text!static/scripts/templates/login_template.html'],
  (template) ->
    class LoginView extends Backbone.View
      events: {}
      render: ->
        @$el.html template
        return @
        # render all sub-views

    return {view: LoginView}
