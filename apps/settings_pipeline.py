PIPELINE_CSS = {
    'core-styles': {
        'source_filenames': (
            'css/layout.scss',
            'css/modules.scss',
            'css/bootstrap-carousel.css',
        ),
        'output_filename': 'compiled/css/core-styles.grouped.css',
        'extra_context': {
            'media': 'all',
        },
    },

    'ie-styles': {
        'source_filenames': (
            'css/ie.less',
        ),
        'output_filename': 'compiled/css/ie.grouped.css',
    },
}

PIPELINE_JS = {
    'core-scripts': {
        'source_filenames': (
            'js/jquery-1.11.0.js',
            'js/carousel.js',
        ),
        'output_filename': 'compiled/js/core-scripts.min.js',
    },
}
