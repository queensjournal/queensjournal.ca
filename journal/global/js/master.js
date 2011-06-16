$(document).ready(function() {
    var queryhash = window.location.hash
    if (queryhash == '#blogs') {
        showBlogs();
    }
    $('.blog-link a').click(showBlogs);
    $('.blog-menu-hide a').click(hideBlogs);
});
function showBlogs() {
    $('#menu-blogs').slideToggle('slow');
}
function hideBlogs() {
    $('#menu-blogs').slideUp(300);
}