/*
 * Journal Mobile Site
 * queensjournal.ca/?flavour=mobile
 *
 * Copyright (c) 2013 Queen's Journal
  */

(function () {
    var global = this;


    // Initial setup
    // =============

    // Map dependancies to local variables
    var $       = global.jQuery;


    // Constructor
    // ===========

    var Journal = (global.Journal || (global.Journal = { }));

    var Mobile = Journal.Mobile = function (options) {
        var defaults = { };

        this.config         = $.extend(true, defaults, options || { });

        this._initialize();
    };


    // Initialization
    // ==============

    Mobile.prototype._initialize = function () {
        this._initializePage();
    };

    Mobile.prototype._initializePage = function () {
        var classnames  = $('body').prop('class').split(' ');
        var index       = classnames.length;

        if (index > 1) {
            while(index--) {
                switch (classnames[index]) {
                    case 'mobile-page':
                        this.initMasonry();
                        break;
                    case 'slider-page':
                        this.initSlider();
                        break;
                }
            }
        }
    };

    Mobile.prototype.initSlider = function () {
        var $slider = this.$slider = $('#slider');

        $slider.anythingSlider({
            expand: false,
            hashtags: false,
            resizeContents: false,
            buildArrows: false,
            buildNavigation: false,
            buildStartStop: false,
            autoPlay: true,
            delay: 5000
        });

        $slider.swipe({
            swipeLeft: function() {
                $slider.data('AnythingSlider').goForward();
                $slider.data('AnythingSlider').startStop(true); },
            swipeRight: function() {
                $slider.data('AnythingSlider').goBack().startStop(true);
                $slider.data('AnythingSlider').startStop(true); },
            threshold: {
                x: 15,
                y: 99999
            },
            preventDefaultEvents: false
        });

    };

    Mobile.prototype.initMasonry = function () {
        var $masonry = this.masonry = $('.jrnl-masonry');

        $(window).load(function () {
            $masonry.masonry({
                singleMode: true,
                columnWidth: 320,
                itemSelector: '.latest-section'
            });
        });
    };

    Journal.mobile = new Mobile();

}).call(this);
