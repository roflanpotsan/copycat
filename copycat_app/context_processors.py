from copycat_app.views import top_tags, top_users


def side_content(request):
    return {'top_tags': top_tags,
            'top_users': top_users}
def current_path(request):
    path = request.path.split('?')[0]
    return {'path': path}

def index_title(request):
    if 'hot' in request.path.split('?')[0]:
        return {'p_title': 'Hot questions'}
    return {'p_title': 'New questions'}