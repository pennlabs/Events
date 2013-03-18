define ['static/javascripts/vendor/text!static/templates/user_template.html'],
  (template) ->
    class UserView extends Backbone.View
      render: ->
        compiled = _.template template, {}
        @$el.html compiled
        return @

    return {view: UserView}
