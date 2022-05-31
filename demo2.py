from h2o_wave import main, app, Q, ui

@app('/demo')
async def serve(q: Q):
    print(q.auth.username)
    
    if not q.client.initialized:
        q.page['meta'] = ui.meta_card(box='', script=ui.inline_script(
            # Handle and transmit event
            'window.onclick = (e) => wave.emit("window", "clicked", { x: e.clientX, y: e.clientY });'
        ))
        q.page['quote'] = ui.markdown_card(
            box='1 1 2 2',
            title='Hello World',
            content='"The Internet? Is that thing still around?" - *Homer Simpson*',)
        q.page['quote2'] = ui.markdown_card(
            box='1 2 2 2',
            title='demo2',
            content='"The Internet? Is that thing still around?" - *Homer Simpson*',)               

        q.client.initialized = True
    else:
        # Capture event
        if q.events.window:
            click = q.events.window.clicked
            if click:
                print(click['x'], click['y'])
        q.page['quote2'].content = f'Clicked at {click["x"]}, {click["y"]}'

    await q.page.save()