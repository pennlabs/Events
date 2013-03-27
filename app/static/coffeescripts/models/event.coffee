define [], ->
  class Event extends Backbone.Model
    idAttribute: "_id"
    defaults:
      name: ''
      time_start: ''
      time_end: ''
      date: ''
      description: ''

  class Events extends Backbone.Collection
    model: Event
    url: '/api/events/'

  return {model: Event, collection: Events}
