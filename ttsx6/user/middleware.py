class UrlMiddleware:
    def process_view(self, request, views_name,views_args, views_kwargs):
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/islogin/',
                                ]:
            request.session['url_path'] = request.get_full_path()


