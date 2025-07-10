import { Constants } from '../utils/Constants'

export function login(username, password) {
    const headers = getHeaders();
    const passwordEncoded = btoa(`${password}`);
    const credentials = btoa(`${username}:${passwordEncoded}`);
    headers.append('Authorization', `Basic ${credentials}`);

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
    const headers = getHeaders();

    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return request(Constants.EVENT, requestOptions);
}

export function addEvent(description) {
    const headers = getHeaders();

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
    const headers = getHeaders();

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

        fetch("http://localhost:8080/".concat(path), requestOptions)
            .then((response) => {
                if (!response.ok) {
                    reject(response.text())
                } else {
                    return response.text()
                }
            })
            .then((result) => {
                resolve(result)
            })
            .catch((error) =>
                reject(error));
    });
}

const getHeaders = () => {
    const headers = new Headers();
    headers.append('Access-Control-Allow-Origin', '*');
    headers.append('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS');
    headers.append('Content-Type', 'application/json');
    headers.append('Access-Control-Allow-Credentials', true);

    return headers;
}