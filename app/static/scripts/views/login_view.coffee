define ['static/scripts/vendor/text!static/scripts/templates/login_template.html'],
  (template) ->
    class LoginView extends Backbone.View
      events:
        'click #register-button' : 'register'
        'click #login-button'    : 'login'
      register: (e) ->
        e.preventDefault()
        $register = $('#register-form')
        $.ajax(
          url: $register.attr('action')
          method: $register.attr('method')
          data: $register.serialize()
        ).done (data) =>
          # fix this on the server side
          data = $.parseJSON data
          if data._id
            @model.set data
            @model.set "logged_in", true
            window.router.navigate '', {trigger: true}
      login: (e) ->
       e.preventDefault()
      render: ->
        @$el.html template
        return @
        # render all sub-views

    return {view: LoginView}
