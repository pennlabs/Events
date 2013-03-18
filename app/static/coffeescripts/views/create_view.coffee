define ['static/javascripts/vendor/text!static/templates/create_template.html'],
  (template) ->
    class CreateView extends Backbone.View
      render: ->
        compiled = _.template template, {}
        @$el.html compiled
        return @

    return {view: CreateView}
