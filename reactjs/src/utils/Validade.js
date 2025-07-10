import { jwtDecode } from 'jwt-decode';
import { Constants } from './Constants'

export const emptyFields = (params) => {
    const email = params.email;
    const password = params.password;

    const emailLength = email.trim().length;
    const passwordLength = password.trim().length;

    return emailLength > 0 && Constants.EMAIL_REGEX.test(email) && passwordLength > 0

}

export const emptyFieldsSignUp = (params) => {
    const password = params.password;
    const repassword = params.repassword;
    
    const minLength = password.length >= 8;
    const hasLowercase = Constants.LOWER_CASE.test(password);
    const hasUppercase = Constants.UPPER_CASE.test(password);
    const hasNumber = Constants.NUMBER.test(password);
    const hasSpecialChar = Constants.SPECIAL_CHAR.test(password);
    const strengthPassoword = minLength && hasLowercase && hasUppercase && hasNumber && hasSpecialChar;

    const strengthCriteria = {
        "minLength": minLength,
        "hasLowercase": hasLowercase,
        "hasUppercase": hasUppercase,
        "hasNumber": hasNumber,
        "hasSpecialChar": hasSpecialChar
    }

    return {
        "buttonDisabled": emptyFields(params) && password === repassword && strengthPassoword,
        "equalPassword": password === repassword,
        strengthCriteria
    };
}

export const validateToken = () => {
        const token = localStorage.getItem("token");
        if (token === "") {
            return null;
        } else {
            const tokenDecoded = jwtDecode(token);
            const currentTime = Date.now() / 1000
            if (tokenDecoded.exp < currentTime) {
                return null;
            }    
            return tokenDecoded;      
        }
}