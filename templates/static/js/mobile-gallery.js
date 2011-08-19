(function( $ ){
    $.fn.mobileGallery = function() {
        $('.galleryback', this).anythingSlider({
            expand: false,
            hashtags: false,
            resizeContents: false,
            buildArrows: false,
            buildNavigation: false,
            buildStartStop: false,
            autoPlay: true,
            delay: 5000,
        });
        $('.galleryback', this).swipe({
            swipeLeft: function() {
                $('#slider').data('AnythingSlider').goForward();
                $('#slider').data('AnythingSlider').startStop(true); },
            swipeRight: function() {
                $('#slider').data('AnythingSlider').goBack().startStop(true);
                $('#slider').data('AnythingSlider').startStop(true); },
            threshold: {
                x: 15,
                y: 99999,
                },
                preventDefaultEvents: false
        });
        var thumbs = $('.thumbs-container', this).find('img');
        function slideStart(thumb_obj) {
            $('.gallerypop', this).show();
        }
        this.bind('click', $.proxy(function() {
            this.slideStart();
        }, this));
    }
})( jQuery );