import web

urls = (
    '/', 'upload'
)

render = web.template.render('templates')


class upload:
    def GET(self):
        return render.index()

    def POST(self):
        return None

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
