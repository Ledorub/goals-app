from rest_framework import renderers


class UserJSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        tokens = {}
        token_fields = tuple(filter(lambda key: key.endswith('_token'), data))
        for name in token_fields:
            tokens[name] = data.pop(name)

        data = {'user': data} if data else {}
        if tokens:
            data['auth'] = tokens
        return super().render(data, accepted_media_type, renderer_context)
