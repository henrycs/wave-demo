from h2o_wave import main, app, Q, ui, on, handle_on



@on('@system.logout')
async def on_user_logout(q: Q):
    print(f'User {q.auth.username} logged out.')


# This function is called when q.args['empty_cart'] is True.
@on(arg='empty_cart')
async def clear_cart(q: Q):
    q.page['cart'].items[0].text.content = 'Your cart was emptied!'
    await q.page.save()


# If the name of the function is the same as that of the q.arg, simply use on().
# This function is called when q.args['buy_now'] is True.
@on()
async def buy_now(q: Q):
    q.page['cart'].items[0].text.content = 'Nothing to buy!'
    await q.page.save()


# This function is called when q.args['#'] is 'about'.
@on(arg='#about')
async def handle_about(q: Q):
    q.page['blurb'].content = 'Everything here is gluten-free!'
    await q.page.save()


# This function is called when q.args['#'] is 'menu/spam', 'menu/ham', 'menu/eggs', etc.
# The 'product' placeholder's value is passed as an argument to the function.
@on(arg='#menu/{product}')
async def handle_menu(q: Q, product: str):
    q.page['blurb'].content = f"Sorry, we're out of {product}!"
    await q.page.save()


@app('/demo')
async def serve(q: Q):
    print("auth", q.auth.username, "token", q.auth.access_token)

    print("user", q.user)
    if q.user.name is None:
        print("q.user.name is not set")
        q.user.name = q.auth.username
        q.client.sid = f"{q.user.name}-sid"
    else:
        print("q.user is ", q.user)
    print("client", q.client)
    print("app", q.app)   

    if not q.client.initialized:
        q.client.initialized = True
        q.page['nav'] = ui.markdown_card(
            box='1 1 4 2',
            title='Menu',
            content='[Spam](#menu/spam) / [Ham](#menu/ham) / [Eggs](#menu/eggs) / [About](#about) /',
        )
        q.page['blurb'] = ui.markdown_card(
            box='1 3 4 2',
            title='Description',
            content='Welcome to our store!',
        )
        q.page['cart'] = ui.form_card(
            box='1 5 4 2',
            title='Cart',
            items=[
                ui.text('Your cart is empty!'),
                ui.buttons([
                    ui.button(name=buy_now.__name__, label='Buy Now!', primary=True),
                    ui.button(name='empty_cart', label='Clear cart'),
                ])
            ],
        )
        q.page['Cat2'] = ui.form_card(
            box='1 7 4 2',
            title='Logout',
            items=[
                ui.link("logout", path="http://192.168.100.201:8080/auth/realms/master/protocol/openid-connect/logout?clientId=wave&userId=9bb0c991-1ce8-4589-ab24-0fa36fd49934")
            ],
        )        

        await q.page.save()
    await handle_on(q)

