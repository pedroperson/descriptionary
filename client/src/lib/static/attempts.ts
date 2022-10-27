// attempts keeps track of all previous attempts made by an user
let attempts: { [key: string]: boolean } = {};

const saveAttempt = (prompt: string) => (attempts[prompt] = true);
const hasAttempted = (prompt: string): boolean => !!attempts[prompt];
const reset = () => (attempts = {});

export default { hasAttempted, saveAttempt, reset };
