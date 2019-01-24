import axios from 'axios';
import config from '../config';
import CBOR from 'cbor-js';
import Cookies from 'js-cookie';
const csrftoken = Cookies.get('csrftoken');

//Where the 
const registerKey = async() => {
    const challenge = await fetch("https://localhost:9000/register/begin", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    const decode = await decodeChallenge(challenge)    
    const encode = await objectSign(decode.response)
    const stat = await registrationStat(encode.response)
    return stat
}

const registrationStat = (response) =>{
    const stat = encode.response ? "Successful" : "Unsuccessful"
    alert('Registration', stat, 'you may now use your key')
}

const decodeChallenge = (response) => {
    if (response.ok) {
        console.log("The response", response)
        const buffer = response.arrayBuffer();
        const decode = CBOR.decode(buffer);
        return navigator.credentials.create(decode)
    }
    else {
        throw new Error('Cannot get registration data')
    }
}

const objectSign = (attestation) => {
    return fetch("https://localhost:9000/register/complete", {
    	method: 'POST',
    	headers: {
    	    'Content-Type': 'application/cbor', 
    		'X-CSRFToken': csrftoken
    	},
    	body: CBOR.encode({
    		"attestationObject": new Uint8Array(attestation.response.attestationObject),
    		"clientDataJSON": new Uint8Array(attestation.response.clientDataJSON),
    	})
    })
}


// const registerKey = () => {
//     fetch("https://localhost:9000/register/begin", {
// 	    method: 'POST',
//         headers: {
//             'X-CSRFToken': csrftoken
//         }
// 	}).then(function(response) {
// 		if(response.ok) {
//             console.log("Fetched")
// 			return response.arrayBuffer();
// 		}
// 	    throw new Error('Error getting registration data!');
				
				
// 	}).then(CBOR.decode).then(function(options) {
// 		//console.log(options, 'response.arraybuff is fine to me')
// 		//This line below is not working
// 		return navigator.credentials.create(options);
// 	}).then(function(attestation) {
// 		//console.log("Start fetch")
// 		return fetch("https://localhost:9000/register/complete", {
// 			method: 'POST',
// 			headers: {
// 				'Content-Type': 'application/cbor', 
// 				'X-CSRFToken': csrftoken
// 			},
// 			body: CBOR.encode({
// 			    "attestationObject": new Uint8Array(attestation.response.attestationObject),
// 				"clientDataJSON": new Uint8Array(attestation.response.clientDataJSON),
// 			})
// 		});
// 		}).then(function(response) {
// 			var stat = response.ok ? 'successful' : 'unsuccessful';
// 			alert('Registration ' + stat + ' More details in server log...');
// 		},function(reason) {
// 			alert(reason);
// 		}).then(function() {
// 			window.location = '/';
//         });
// }
            
export default registerKey;