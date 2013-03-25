define ['static/javascripts/vendor/text!static/templates/event_template.html'],
  (template) ->
    class EventView extends Backbone.View
      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: EventView}
