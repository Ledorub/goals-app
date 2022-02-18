const USE_HTTPS = false

const HOST = `${USE_HTTPS ? 'https' : 'http'}://127.0.0.1`
const PORT = 8000


export const baseURL = new URL('app/', `${HOST}:${PORT}`)