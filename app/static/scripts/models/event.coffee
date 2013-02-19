define [], ->
  class Event extends Backbone.Model
    defaults:
      name: ''
      description: ''

  class Events extends Backbone.Collection
    model: Event
    url: '/events'

  return {model: Event, collection: Events}
