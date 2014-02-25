function setActiveStyleSheet(title) {  // select the stylesheet
    var i, a, main;
    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
        if(a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title")) {
            a.disabled = true;
            if(a.getAttribute("title") == title) a.disabled = false;
        }
    }
}

function add_preview_message() {
    var x,y;
    if (self.innerHeight) // all except Explorer
    {
        x = self.innerWidth;
        y = self.innerHeight;
    }
    else if (document.documentElement && document.documentElement.clientHeight)
        // Explorer 6 Strict Mode
    {
        x = document.documentElement.clientWidth;
        y = document.documentElement.clientHeight;
    }
    else if (document.body) // other Explorers
    {
        x = document.body.clientWidth;
        y = document.body.clientHeight;
    }
    
    var doc_x, doc_y;
    var test1 = document.body.scrollHeight;
    var test2 = document.body.offsetHeight
    if (test1 > test2) // all but Explorer Mac
    {
        doc_x = document.body.scrollWidth;
        doc_y = document.body.scrollHeight;
    }
    else // Explorer Mac;
         //would also work in Explorer 6 Strict, Mozilla and Safari
    {
        doc_x = document.body.offsetWidth;
        doc_y = document.body.offsetHeight;
    }
    var body = document.getElementsByTagName('body')[0];
    
    // build message div
    var preview_msg = document.createElement('div');
    preview_msg.id = 'print-preview-dialog';
    preview_msg.style.width = x/2 + 'px';
    preview_msg.style.top = y/3 + 'px';
    preview_msg.style.left = x/4 + 'px';
    
    var preview_head = document.createElement('h3');
    preview_head.appendChild(document.createTextNode('The article is ready to print.'));
    var preview_body = document.createElement('p');
    preview_body.appendChild(document.createTextNode('The article has been reformatted for optimal printing. This message will not appear on the final printed page(s).'));
    var preview_return_link = document.createElement('a');
    preview_return_link.appendChild(document.createTextNode('Return to the Journal site.'));
    preview_return_link.onclick = function() { cancel_print_preview(); return false; };
    preview_return_link.href = '#';
    
    preview_msg.appendChild(preview_head);
    preview_msg.appendChild(preview_body);
    preview_msg.appendChild(preview_return_link);
    
    // build overlay
    var overlay = document.createElement('div');
    overlay.id = 'overlay';
    overlay.style.height = (doc_y > y ? doc_y : y) + 'px';
    overlay.style.width = (doc_x > x ? doc_x : x) + 'px';
    
    // add elements to body
    body.appendChild(overlay);
    body.appendChild(preview_msg);
}

function cancel_print_preview() {
    var preview_msg = document.getElementById('print-preview-dialog');
    var overlay = document.getElementById('overlay');
    var body = document.getElementsByTagName('body')[0];
    body.removeChild(preview_msg);
    body.removeChild(overlay);
    setActiveStyleSheet('Default');
}

function print_preview() {
    // set print stylesheet
    setActiveStyleSheet('Print Preview');
    
    // show preview message
    add_preview_message();
    
    // print the page
    window.print();
}
