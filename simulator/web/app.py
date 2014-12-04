import web

urls = (
    '/', 'upload'
)

render = web.template.render('templates')


class upload:
    def GET(self):
        return render.index()

    def POST(self):
        code = web.input().get("algorithm", "")
        write_algorithm(code)
        return "Cool bro"


def write_algorithm(code):
    file = open("uploads/algorithm.py", "wb")
    file.write(code)
    file.close()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
