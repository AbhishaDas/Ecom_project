# context_processors.py
def user_id_processor(request):
    return {
        'user_id': request.session.get('user_id')
    }