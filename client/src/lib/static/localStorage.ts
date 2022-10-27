export const newLocalStorageLayer = (key: string, defaultValue: any): LocalStorage => {
	if (typeof window === 'undefined') {
		return mockLocalStorage(defaultValue);
	}

	return newStorageLayerGenerator(localStorage)(key, defaultValue);
};

interface LocalStorage {
	read: () => any;
	write: (value: any) => void;
}

const mockLocalStorage = (defaultValue: any) => ({
	read: () => defaultValue,
	write: () => {
		// do nothing
	}
});

// newStorageLayerGenerator is a curried version of the StorageLayer class.
const newStorageLayerGenerator =
	(storage: Storage) =>
	(key: string, defaultValue: any): StorageLayer => {
		return new StorageLayer(storage, key, defaultValue);
	};

// StorageLayer contains a storage object (with methods getItem(string):string and  setItem(string,string)), and key it uses to access the storage
class StorageLayer {
	storage: Storage;
	key: string;
	defaultValue: any;

	constructor(storage: Storage, key: string, defaultValue: any) {
		this.storage = storage;
		this.key = key;
		this.defaultValue = defaultValue;
	}

	read() {
		const stringFromStorage = this.storage.getItem(this.key);
		if (stringFromStorage === null) return this.defaultValue;
		return stringToObject(stringFromStorage);
	}

	write(value: any) {
		this.storage.setItem(this.key, objectToString(value));
	}
}

const stringToObject = (str: string) => JSON.parse(str);
const objectToString = (obj: any) => JSON.stringify(obj);
