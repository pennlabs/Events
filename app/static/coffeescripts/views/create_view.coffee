define ['/static/javascripts/vendor/text.js!/static/templates/create_template.html'],
  (template) ->
    class CreateView extends Backbone.View
      events:
        'click #submit-button' : 'create_event'
      submit_form: ($form, success) ->
        $.ajax(
          url: $form.attr 'action'
          method: $form.attr 'method'
          data: $form.serialize()
        ).done success

      create_event: (e) ->
        e.preventDefault()
        $create = $('#create-form')
        @submit_form $create, (event) =>
          event = $.parseJSON event
          @collection.add event
          events = _.clone @model.get('events')
          events.push event._id
          @model.set("events", events)
          window.router.navigate '', {trigger: true}
      render: ->
        compiled = _.template template, {}
        @$el.html compiled
        return @

    return {view: CreateView}
