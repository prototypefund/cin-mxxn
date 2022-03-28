
export class IconLoadError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'IconLoadError'
  }
}
