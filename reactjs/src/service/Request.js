import { Constants } from '../utils/Constants'

export function login(username, password) {
    const passwordEncoded = btoa(`${password}`);
    const credentials = btoa(`${username}:${passwordEncoded}`);
    const headers = getHeaders(`Basic ${credentials}`);

    const requestOptions = {
        method: 'POST',
        headers: headers
    };
    return request(Constants.LOGIN, requestOptions);
}

export function signUp(username, password) {
    const headers = getHeaders();
    const passwordEncoded = btoa(`${password}`);

    const body = {
        "email": username,
        "password": passwordEncoded
    }

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    };

    return request(Constants.SIGN_UP, requestOptions);
}

export function getEvents() {
    const token = localStorage.getItem("token");
    const headers = getHeaders(`Bearer ${token}`);

    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return request(Constants.EVENT, requestOptions);
}

export function addEvent(description) {
    const token = localStorage.getItem("token");
    const headers = getHeaders(`Bearer ${token}`);

    const body = {
        "description": description
    }

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    };

    return request(Constants.EVENT, requestOptions);
}

export function deleteEvent(id) {
    const token = localStorage.getItem("token");
    const headers = getHeaders(`Bearer ${token}`);

    const body = {
        "id": id
    }

    const requestOptions = {
        method: 'DELETE',
        headers: headers,
        body: JSON.stringify(body)
    };

    return request(Constants.EVENT, requestOptions);
}

const request = (path, requestOptions) => {
    return new Promise((resolve, reject) => {
        const apiUrl = process.env.REACT_APP_API_URL;
        fetch(apiUrl.concat(path), requestOptions)
            .then((response) => {
                if (response.status === 200 || response.status === 201) {
                    return response.text()
                } else if (response.status === 500) {
                    //to-do
                    reject('Internal Error')
                } else {
                    reject(response.text())
                }
            })
            .then((result) => {
                resolve(result)
            })
            .catch((error) => 
                reject(error.message));
    });
}

const getHeaders = (authorization) => {
    const headers = new Headers();
    headers.append('Access-Control-Allow-Origin', '*');
    headers.append('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS');
    headers.append('Content-Type', 'application/json');
    headers.append('Access-Control-Allow-Credentials', true);
    headers.append('Authorization', authorization);

    return headers;
}