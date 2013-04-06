PIPELINE_CSS = {
    'core-styles': {
        'source_filenames': (
            'css/blueprint/reset.css',
            'css/blueprint/liquid.css',
            'css/screen.less',

            'css/modules.less',
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
            'js/jquery-1.6.1.min.js',
            'js/master.js',
        ),
        'output_filename': 'compiled/js/core-scripts.min.js',
    },

    'mobile-scripts': {
        'source_filenames': (
            'js/jquery.masonry.js',
            'js/jquery.anythingslider.min.js',
            'js/jquery.swipe.js',
            'js/mobile.js',
        ),
        'output_filename': 'compiled/js/mobile-scripts.min.js',
    },
}
