//Where MDC web components are initialized!


//Initialize all textfields to use 
var textFields = document.querySelectorAll('.mdc-text-field');
for(var i = 0; i < textFields.length; i++) {
	mdc.textField.MDCTextField.attachTo(textFields[i]);
}
