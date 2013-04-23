define ['/static/javascripts/vendor/text.js!/static/templates/event_template.html'],
  (template) ->
    class EventView extends Backbone.View
      className: 'card'
      events:
        'click a.creator': 'show_user'
        'click a.event'  : 'show_event'
      show_user: (e) ->
        e.preventDefault()
        window.router.navigate "user/#{@model.get("creator")}", {trigger: true}
      show_event: (e) ->
        e.preventDefault()
        window.router.navigate "event/#{@model.id}", {trigger: true}
      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: EventView}
