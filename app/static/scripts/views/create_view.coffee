define ['static/scripts/vendor/text!static/scripts/templates/create_template.html'],
  (template) ->
    class CreateView extends Backbone.View
      render: ->
        compiled = _.template template, null
        @$el.html compiled
        return @

    return {view: CreateView}
