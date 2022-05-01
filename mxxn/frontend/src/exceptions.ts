
class RequestError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RequestError';
  }
}


class IconLoadError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'IconLoadError';
  }
}


class ThemeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ThemeError';
  }
}

class StringsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'StringsError';
  }
}

export{
  RequestError,
  IconLoadError,
  ThemeError,
  StringsError
};
