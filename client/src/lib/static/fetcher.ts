export async function post(url: string, data = {}) {
	return fetch(url, params(data)).then((res) => {
		if (!res.ok) {
			throw responseError(res);
		}
		return res.text();
	});
}

export async function postToJSON(url: string, data = {}) {
	return fetch(url, params(data)).then((res) => {
		if (!res.ok) {
			throw responseError(res);
		}
		return res.json();
	});
}
export async function GET(url: string) {
	return fetch(url, { method: 'GET' }).then((res) => {
		if (!res.ok) {
			throw responseError(res);
		}
		return res.text();
	});
}

export const responseError = (res: Response) => new Error(httpError(res.status) || res.statusText);

const params = (body = {}): RequestInit => ({
	method: 'POST',
	headers: {},
	body: JSON.stringify(body)
});

const paramsGET = (): RequestInit => ({
	method: 'GET',
	credentials: 'same-origin',
	headers: {
		'Content-Type': 'application/json',
		Accept: 'application/json'
	}
});

const httpError = (code: number) =>
	({
		400: 'invalid form data. Make sure all fields were properly filled out',
		401: 'you are not authorized to access this resource',
		404: 'the endpoint you are trying to reach was not found',
		429: 'your request was blocked because it was repeated too many times. Try again later',
		500: 'internal server error'
	}[code]);
