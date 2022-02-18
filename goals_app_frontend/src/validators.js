export function minLengthValidator(len) {
    return value => value && value.length >= len
}