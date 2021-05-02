import Model
# Driver Function
if __name__ == '__main__':
    try:
        # intiating Model
        model = Model.Model()
        # calling for heroku
        model._run_heroku()
    except Exception as e:
        print("App Error:  ", e)

    print("App Closes.")
