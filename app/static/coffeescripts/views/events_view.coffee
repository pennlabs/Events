define ['/static/javascripts/views/event_view.js'],
  (EventView) ->
    class EventsView extends Backbone.View
      render: ->
        views = []
        @collection.each (event) ->
          event_view = new EventView.view(model: event)
          views.push event_view.render()
        viewEls = _.pluck views, 'el'
        @$el.html viewEls
        return @

    return {view: EventsView}
