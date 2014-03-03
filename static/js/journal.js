// Generated by CoffeeScript 1.7.1
(function() {
  $(function() {
    var $carousel, calcCarouselHeight;
    $carousel = $('.carousel');
    calcCarouselHeight = function() {
      var $slides, heights;
      $slides = $carousel.find('.item');
      heights = [];
      $slides.each(function(i, obj) {
        return heights.push($(obj).height());
      });
      return $carousel.height(_.max(heights) + 'px');
    };
    if ($carousel.length) {
      return $(window).load(calcCarouselHeight);
    }
  });

}).call(this);
