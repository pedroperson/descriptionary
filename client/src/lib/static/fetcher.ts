export async function post(url: string, data = {}) {
	return fetch(url, params(data))
		.then((res) => {
			if (!res.ok) {
				throw responseError(res);
			}
			return res.json();
		})
		.then((json) => {
			if (json.error) {
				throw json.error;
			}
			return json;
		});
}

export const responseError = (res: Response) => new Error(httpError(res.status) || res.statusText);

const params = (body = {}): RequestInit => ({
	method: 'POST',
	credentials: 'same-origin',
	headers: {
		'Content-Type': 'application/json',
		Accept: 'application/json'
	},
	body: JSON.stringify(body)
});

const httpError = (code: number) =>
	({
		400: 'invalid form data. Make sure all fields were properly filled out',
		401: 'you are not authorized to access this resource',
		404: 'the endpoint you are trying to reach was not found',
		429: 'your request was blocked because it was repeated too many times. Try again later',
		500: 'internal server error'
	}[code]);
