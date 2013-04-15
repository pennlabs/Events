define ['/static/javascripts/vendor/text.js!/static/templates/user_template.html'],
  (template) ->
    class UserView extends Backbone.View
      events:
        'click a.subscribe' : 'subscribe'
      subscribe: (e) ->
        e.preventDefault()
        window.router.user.subscribe @model
      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: UserView}
