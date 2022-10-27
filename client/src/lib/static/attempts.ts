// attempts keeps track of all previous attempts made by an user
const attempts: { [key: string]: boolean } = {};

const newAttempt = (prompt: string) => (attempts[prompt] = true);
const hasAttempted = (prompt: string): boolean => !!attempts[prompt];

export default { hasAttempted, newAttempt };
