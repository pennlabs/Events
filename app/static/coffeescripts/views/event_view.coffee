define ['static/scripts/vendor/text!static/scripts/templates/event_template.html'],
  (template) ->
    class EventView extends Backbone.View
      render: ->
        compiled = _.template template, null
        @$el.html compiled
        return @

    return {view: EventView}
