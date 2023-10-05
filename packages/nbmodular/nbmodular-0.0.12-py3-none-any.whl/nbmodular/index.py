def my_new_function():
    my_new_local = 3
    my_other_new_local = 4
def my_second_new_function():
    my_second_variable = 100
    my_second_other_variable = 200

def index_pipeline (test=False, load=True, save=True, result_file_name="index_pipeline"):

    # load result
    result_file_name += '.pk'
    path_variables = Path ("index") / result_file_name
    if load and path_variables.exists():
        result = joblib.load (path_variables)
        return result

    my_new_function ()
    my_second_new_function ()

    # save result
    result = Bunch ()
    if save:    
        path_variables.parent.mkdir (parents=True, exist_ok=True)
        joblib.dump (result, path_variables)
    return result
