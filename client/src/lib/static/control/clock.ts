type milliseconds = number;

export function Clock(
	numSteps: number,
	stepDuration: milliseconds,
	everyStep: () => void,
	onEnd: () => void
) {
	let ticker: NodeJS.Timer | null = null;
	let counter = 0;

	const stop = () => {
		if (ticker !== null) clearInterval(ticker);
	};

	return {
		start: () => {
			stop();

			ticker = setInterval(() => {
				if (counter >= numSteps) {
					stop();
					onEnd();
					return;
				}

				counter += 1;
				everyStep();
			}, stepDuration);
		}
	};
}
