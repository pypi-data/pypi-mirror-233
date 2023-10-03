def data():
    a=1
    b=2
    return a,b
def add_function(a, b):
    c = a+b
    return c

def test_tutorial_pipeline (test=False, load=True, save=True, result_file_name="test_tutorial_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("test_tutorial") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    a, b = data ()
    c = add_function (a, b)

    # save result
    result = Bunch (a=a,c=c,b=b)
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
