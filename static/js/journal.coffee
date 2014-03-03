$( () ->

  $carousel = $('.carousel')

  calcCarouselHeight = () ->
    $slides = $carousel.find '.item'
    heights = []

    $slides.each (i, obj) ->
      heights.push($(obj).height())

    $carousel.height(_.max(heights) + 'px')

  if $carousel.length
    $(window).load( calcCarouselHeight )
)
