$(document).ready(function() {
    var queryhash = window.location.hash
    if (queryhash == '#blogs') {
        toggleBlogs();
        $('#blog-menu-arrow').show();
    }
    var num_blogs = $('.menu-blog').size()
    $('#menu-blogs-scroll').css('width', (num_blogs * 225) + 'px')
    $('.blog-link a span').append('<div id="blog-menu-arrow"></div>');
    $('.blog-link a').click(toggleBlogs);
    $('.blog-menu-hide a').click(hideBlogs);
});
function toggleBlogs() {
    if ($('#menu-blogs').hasClass('active')) {
        hideBlogs();
    } else {
        $('#menu-blogs').slideDown(500).addClass('active')
        $('#menu-sections').delay(300).css('margin-bottom', '0.5em');
        $('#blog-menu-arrow').show();
    }
}
function hideBlogs() {
    $('#menu-blogs').slideUp(300);
    $('#menu-blogs').removeClass('active')
    $('#menu-sections').css('margin-bottom', '1.5em');
    $('#blog-menu-arrow').hide();
}