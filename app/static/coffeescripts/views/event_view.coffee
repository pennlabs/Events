define ['/static/javascripts/vendor/text.js!/static/templates/event_template.html'],
  (template) ->
    class EventView extends Backbone.View
      events:
        'click a.creator': 'show_user'
      show_user: (e) ->
        e.preventDefault()
        window.router.navigate "user/#{@model.get("creator")}", {trigger: true}
      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: EventView}
