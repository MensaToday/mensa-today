const defaultFetchParams = {
    cache: 'no-cache',
    mode: 'cors',
    referrerPolicy: 'no-referrer',
    credentials: 'include',
}

class API {
    #auth = {
        access: null,
        refresh: null
    }
    #endpoint = "http://localhost:9999"

    post = async (params) => this.request({ method: 'POST', ...params})
    get = async (params) => this.request({ method: 'GET', ...params})
    request = async ({method, url, unauthenticated, json}) => {
        console.log(method, url, unauthenticated, json)
        const headers = {
            'Content-Type': 'application/json',
        }
    
        if (!unauthenticated) {
            headers['Authorization'] =  `Bearer ${this.#auth.access}`
        }
        
        const fetchParams = {
            method,
            ...defaultFetchParams,
            headers,
        }

        if (json) {
            fetchParams.body = JSON.stringify(json) 
        }

        const response = await fetch(url, fetchParams);
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(await response.text())
        }
    }

    register = async (user) => {
        return await this.post({
            url: `${this.#endpoint}/api/v1/user/register`, 
            unauthenticated: true,
            json: user,
        })
    }

    login = async (user) => {
        const authTokens = await this.post({
            url: `${this.#endpoint}/api/v1/user/login`, 
            json: user,
        })

        this.#auth = authTokens
        return authTokens
    }

    logout = async () => {
        const resp = await this.post({
            url: `${this.#endpoint}/api/v1/user/logout`, 
            json: {'refresh_token': this.#auth.refresh},
        })

        this.#auth = {
            access: null,
            refresh: null
        }
        return resp
    }

    getBalance = async () => {  
        await this.get({
            url: `${this.#endpoint}/api/v1/user/get_balance`, 
        })
    }

    getDishPlan = async () => {  
        await this.get({
            url: `${this.#endpoint}/api/v1/mensa/get_dishplan`, 
        })
    }
}

export const api = new API()