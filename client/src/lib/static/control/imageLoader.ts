export async function loadImages(srcs: string[]): Promise<HTMLImageElement[]> {
	const results = await Promise.allSettled(srcs.map(loadImage)).then((values) =>
		values.map((v) => {
			if (v.status === 'fulfilled') return v.value;
			return null;
		})
	);

	return results.filter((v): v is Exclude<typeof v, null> => v !== null);
}

async function loadImage(src: string): Promise<HTMLImageElement> {
	return new Promise((resolve, reject) => {
		const image = new Image();

		image.onload = function () {
			resolve(image);
		};

		image.onerror = (event) => {
			console.log('Could not load image', event);
			image.src = '';
			reject(image);
		};

		image.src = src;
	});
}
