from h2o_wave import main, app, Q, ui, on, handle_on



@on('@system.logout')
async def on_user_logout(q: Q):
    print(f'User {q.auth.username} logged out.')

@on('#test')
async def on_test(q: Q):
    print("q.client.initialized in test: ", q.client.initialized)
    q.


@app('/demo')
async def serve(q: Q):
    print("auth", q.auth.username, "token", q.auth.access_token)
    if q.user.name is None:
        print("q.user.name is not set")
        q.user.name = q.auth.username
    else:
        print("q.user is ", q.user)
    print("q.client.initialized: ", q.client.initialized)

    if not q.client.initialized:
        q.client.initialized = True
        q.page['nav'] = ui.form_card(
            box='1 1 4 2',
            title='Menu',
            items=[
                ui.button(label=q.user.name, name='#test'),
                ui.link(label='Logout', path='_auth/logout', target=''),            
            ]
        )
        
        await handle_on(q)
        
        #http://192.168.100.201:8080/auth/realms/master/protocol/openid-connect/logout?clientId=wave&userId=9bb0c991-1ce8-4589-ab24-0fa36fd49934', target='_blank
        
        await q.page.save()
    

