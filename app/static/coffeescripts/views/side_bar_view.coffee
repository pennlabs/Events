define ['/static/javascripts/vendor/text.js!/static/templates/side_bar_template.html'],
  (template) ->
    class SideBarView extends Backbone.View
      className: 'sidebar'
      render: ->
        @$el.html template
        return @

    return {view: SideBarView}
