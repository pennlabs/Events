define ['static/scripts/vendor/text!static/scripts/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events: {}
      render: ->
        @$el.html template
        return @
        # render all sub-views

    return {view: MainView}
