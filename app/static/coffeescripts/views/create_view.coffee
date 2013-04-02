define ['/static/javascripts/vendor/text.js!/static/templates/create_template.html'],
  (template) ->
    class CreateView extends Backbone.View
      events:
        'click #submit-button' : 'create_event'

      create_event: (e) ->
        e.preventDefault()
        event = $('#create-form').serializeObject()
        event.creator = @model.id
        event.creator_name = @model.get("name")
        @collection.create event
        window.router.navigate '', {trigger: true}

      render: ->
        compiled = _.template template, {}
        @$el.html compiled
        return @

    return {view: CreateView}
