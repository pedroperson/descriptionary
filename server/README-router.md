# Router

The router will handle http messages.

## Routing

I kinda want an interface like:

```
router.GET("/a/b/", handleAB) (?maybe pass the type here?)

def handleAB(data:dict[str,any], writer : Writer):
    guess = mydata['guess']
    guess_index = guess[0]
    writer.send_result(guess_index)

Writer {
    send_result(Any)
    send_success()
    send_error(error)
}
```

I want to sign every route up, but not process them right away. Then we we run the RUN command, we process every route into a node tree. Searching that tree should be BLAZINGLY FAST!!!
