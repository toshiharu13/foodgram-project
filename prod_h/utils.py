import importlib
module = importlib.import_module('.settings', 'foodgram-project')

def get_tags(request):
    # Get tags list
    tags_list = []
    for key in request.POST.keys():
        if key in module.TAGS:
            tags_list.append(key)
    return tags_list