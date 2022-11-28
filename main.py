from FlaskAPI import Build_App


app = Build_App()


if __name__ == '__main__':
    app.run(debug=True)