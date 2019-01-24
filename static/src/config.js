import axios from 'axios';
import Cookies from 'js-cookie';

let csrftoken = Cookies.get('csrftoken');
const config = axios.create({
    baseURL: 'https://localhost:9000/'
})
config.defaults.headers.common['X-CSRF-TOKEN'] = csrftoken;

export default config;