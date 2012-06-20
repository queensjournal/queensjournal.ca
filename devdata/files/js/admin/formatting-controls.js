/* addTags. Adds a pair of opening/closing tags around selected text.
	tag: String. Name of HTML tag to add (em, strong, h2).
	textarea: HTML node. Textarea element with target text. Used to check if selection is in target.
	params: Array. List of keypairs--
		params[a] (where a % 2 == 0) is the parameter (href, class, id);
		params[a+1] is the value passed to the parameter (a URL for href, etc.).
*/
	
function addTags(tag, textarea, params) {
	// construct tag elements
	var startTag = '';
	var endTag = '';
	var tagParams = '';
	if(params != null && params.length) {
		for(var i = 0; i < params.length; i+=2) {
			tagParams += ' ' + params[i] + '="' + params[i+1] + '"';
		}
	}
	startTag = '<' + tag;
	if(tagParams != '') {
		startTag += tagParams;
	}
	startTag += '>';
	endTag = '</' + tag + '>';

	// check for IE
	if(document.selection) {
		var range = document.selection.createRange();
		if(range.parentElement() == textarea && range.text != '') {
			document.selection.createRange().text = startTag + range.text + endTag;
		}
	}
	else if(textarea.selectionStart < textarea.selectionEnd) {
		// get initial textarea status
		var finalCursor = textarea.selectionEnd + startTag.length;
		var scrollTop = textarea.scrollTop;
		var scrollLeft = textarea.scrollLeft;
		
		var textPrefix = textarea.value.substr(0, textarea.selectionStart);
		var textSuffix = textarea.value.substr(textarea.selectionEnd);
		var range = textarea.value.substr(textarea.selectionStart, textarea.selectionEnd - textarea.selectionStart);
		textarea.value = textPrefix + startTag + range + endTag + textSuffix;
		textarea.focus();
		textarea.setSelectionRange(finalCursor, finalCursor);
		textarea.scrollTop = scrollTop;
		textarea.scrollLeft = scrollLeft;
	}
}

/* addList. Creates a list out of a selection of lines.
	ordered: boolean. True for ordered list, False for unordered list.
	textarea: HTML node. Textarea element with target text. Used to check if selection is in target.
	params: Array. List of keypairs--
		params[a] (where a % 2 == 0) is the parameter (href, class, id);
		params[a+1] is the value passed to the parameter (a URL for href, etc.).
*/
function addList(ordered, textarea, params) {
	// construct tag elements
	var startList = '';
	var endList = '';
	var tagParams = '';
	if(params != null && params.length) {
		for(var i = 0; i < params.length; i+=2) {
			tagParams += ' ' + params[i] + '="' + params[i+1] + '"';
		}
	}
	startList = '<' + (ordered ? 'ol' : 'ul');
	if(tagParams != '') {
		startList += tagParams;
	}
	startList += '>';
	endList = '</' + (ordered ? 'ol' : 'ul') + '>';

	// check for IE
	if(document.selection) {
		var range = document.selection.createRange();
		if(range.parentElement() == textarea && range.text != '') {
			document.selection.createRange().text = startList + insertListItems(range.text) + endList;
		}
	}
	else if(textarea.selectionStart < textarea.selectionEnd) {
		// get initial textarea status
		var finalCursor = textarea.selectionEnd + startList.length;
		var scrollTop = textarea.scrollTop;
		var scrollLeft = textarea.scrollLeft;
		
		var textPrefix = textarea.value.substr(0, textarea.selectionStart);
		var textSuffix = textarea.value.substr(textarea.selectionEnd);
		var range = textarea.value.substr(textarea.selectionStart, textarea.selectionEnd - textarea.selectionStart);
		textarea.value = textPrefix + startList + insertListItems(range) + endList + textSuffix;
		textarea.focus();
		textarea.setSelectionRange(finalCursor, finalCursor);
		textarea.scrollTop = scrollTop;
		textarea.scrollLeft = scrollLeft;
	}
}

function insertListItems(text) {
	return text.replace(/^(.+)$/gm, '<li>$1</li>');
}

/* attach_textareas. Attaches a set of formatting controls to every textarea.
	No parameters.
*/
function attachTextareas() {
	// get all textareas
	var fieldsets = document.getElementsByTagName('fieldset');
	var allAreas = document.getElementsByTagName('textarea');
	var textareas = new Array();
	for(var i = 0; i < fieldsets.length; i++) {
		if(fieldsets[i].className.search(/richedit/) != -1) {
			var temp_areas = fieldsets[i].getElementsByTagName('textarea');
			for(var j = 0; j < temp_areas.length; j++) {
				textareas.push(new Array(temp_areas[j], 'RE'));
			}
		}
	}
	for(var i = 0; i < allAreas.length; i++) {
		if(allAreas[i].id.search(/factbox/) != -1) {
			textareas.push(new Array(allAreas[i], 'IN'));
		}
	}
	// var textareas = document.getElementsByTagName('textarea');
	
	// set up button
	var genButton = document.createElement('input');
	genButton.type = 'button';
	genButton.style.float = 'left';
	genButton.style.marginRight = '1em';
	
	// create buttons for every textarea
	for(var i = 0; i < textareas.length; i++) {
		// create button container
		var buttonContainer = document.createElement('div');
		if(textareas[i][1].search(/RE/) != -1) {
			buttonContainer.style.marginLeft = '10em';
		}
		buttonContainer.className = textareas[i][1];
		
		// create reflow button
		var reflowButton = genButton.cloneNode(true);
		reflowButton.value = 'Reflow text';
		reflowButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			if(targetTextarea.value.search(/\n[^\r]/) != -1) { // doesn't work, maybe remove condition entirely?
				var fieldContent = targetTextarea.value;
				fieldContent = fieldContent.replace(/(\r?\n){2,}/gm, "\r\n");
				fieldContent = fieldContent.replace(/([^\.\?!"]) \r?\n/gm, "$1 ");
				fieldContent = fieldContent.replace(/ ?\r?\n/gm, "\r\n\r\n");
				targetTextarea.value = fieldContent;
			}
			else {
				alert('You\'ve already reflowed the text!');
			}
		};
		
		// create style buttons
		var subheadButton = genButton.cloneNode(true);
		subheadButton.value = 'Subheading';
		subheadButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			addTags('h4', targetTextarea, null);
		};

		var strongButton = genButton.cloneNode(true);
		strongButton.value = 'B';
		strongButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			addTags('strong', targetTextarea, null);
		};
		
		var emButton = genButton.cloneNode(true);
		emButton.value = 'I';
		emButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			addTags('em', targetTextarea, null);
		};

		var anchorButton = genButton.cloneNode(true);
		anchorButton.value = 'link';
		anchorButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			var hrefURL = window.prompt('Please enter the URL for the link. (ex. "http://www.google.com/")', 'http://');
			if(hrefURL != null && hrefURL != 'http://') {
				addTags('a', targetTextarea, new Array('href', hrefURL));
			}
		};
		
		var uListButton = genButton.cloneNode(true);
		uListButton.value = 'Convert to plain list';
		uListButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			addList(false, targetTextarea, null);
		};
		
		var oListButton = genButton.cloneNode(true);
		oListButton.value = 'Convert to numbered list';
		oListButton.onclick = function() {
			var targetTextarea = this.parentNode.parentNode.getElementsByTagName('textarea')[0];
			addList(true, targetTextarea, null);
		};

		// add buttons to button container
		buttonContainer.appendChild(reflowButton);
		buttonContainer.appendChild(subheadButton);
		buttonContainer.appendChild(strongButton);
		buttonContainer.appendChild(emButton);
		buttonContainer.appendChild(anchorButton);
		buttonContainer.appendChild(uListButton);
		buttonContainer.appendChild(oListButton);
		
		// add container to admin form, just below textarea
		textareas[i][0].parentNode.appendChild(buttonContainer);
	}
}

addEvent(window, 'load', attachTextareas);