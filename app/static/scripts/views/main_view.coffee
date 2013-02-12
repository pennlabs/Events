define ['static/scripts/vendor/text!static/scripts/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      initialize: ->
        @$el.html template
      events: {}

    return {view: MainView}
