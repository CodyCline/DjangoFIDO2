import registerKey from './accounts/add-key';
import { MDCMenu } from '@material/menu/index';
// import {MDCButton} from '@material/button/index';
import { MDCTextField } from '@material/textfield';
import './layout.scss'

const textFields = document.querySelectorAll('.mdc-text-field');
console.log(textFields)

for (const text of textFields) {
  MDCTextField.attachTo(text);
}

// mdc.textFields.MDCTextField.attachTo(document.querySelector('.mdc-text-field'));

const buttons = document.querySelectorAll('.mdc-button');

const menu = document.querySelector('.mdc-list');



window.registerKey = registerKey;