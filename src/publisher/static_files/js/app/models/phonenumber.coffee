#
# Telephone
# ---------
#
class publisher.models.Phonenumber extends Backbone.Model

  defaults:
    id: ""

  url: ->
    console.log @.get('profile')
    # profile_id = @.get('profile_id')
    return "/api/1.0/account/profile/phonenumbers/#{id}/?format=json"

#
# PhonenumberList 
# -------------
#
class publisher.models.PhonenumberList extends Backbone.Collection

  url: ->
    return "/api/1.0/account/profile/phonenumbers/?format=json"
