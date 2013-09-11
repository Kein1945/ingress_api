ingress_api
===========

Ingress api

Usage:

    rpc = ingress.rpc('var/cookie.file', token, debug=true|false)
    messages = ingress.chat(rpc)
    data = messages.retrive(30) // Retrive 30 last messages
    sender = ingress.message(rpc)
    sender.send("some text")
