import registerKey from './accounts/add-key';
// import { MDCMenu } from '@material/menu';

// const menu = new MDCMenu(document.querySelector('.mdc-list'));

const menu = document.getElementsByClassName('.menu-toggle');

console.log(menu)

const menuToggleOpen = () => {
    menu.open = true;
}

const menuToggleClose = () => {
    menu.open = false;
}

window.menuToggleClose = menuToggleClose;
window.menuToggleOpen = menuToggleOpen;
window.registerKey = registerKey;