from branca.element import Figure, Element, JavascriptLink, CssLink


class JSCSSMixin(Element):
    """Render links to external Javascript and CSS resources."""

    _default_js = [
        ('leaflet',
        'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js'),
        ('jquery',
        'https://code.jquery.com/jquery-1.12.4.min.js'),
        ('bootstrap',
        'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
        ('awesome_markers',
        'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js'),  # noqa
        ]

    _default_css = [
        ('leaflet_css',
        'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css'),
        ('bootstrap_css',
        'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'),
        ('bootstrap_theme_css',
        'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css'),  # noqa
        ('awesome_markers_font_css',
        'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),  # noqa
        ('awesome_markers_css',
        'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),  # noqa
        ('awesome_rotate_css',
        'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css'),  # noqa
        ]

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        for name, url in self.default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

        for name, url in self.default_css:
            figure.header.add_child(CssLink(url), name=name)

        super().render(**kwargs)
