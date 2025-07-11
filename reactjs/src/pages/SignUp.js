import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { signUp } from '../service/Request'
import Alert from 'react-bootstrap/Alert';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ModalComponent from '../components/ModalComponent'
import { emptyFieldsSignUp } from '../utils/Validade'
import { Constants } from '../utils/Constants'

const SignUp = () => {

    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repassword, setRePassword] = useState('');
    const [buttonDisabled, setButtonDisabled] = useState(true)
    const [error, setError] = useState(false)
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState(null);

    const [strength, setStrength] = useState({
        minLength: false,
        hasLowercase: false,
        hasUppercase: false,
        hasNumber: false,
        hasSpecialChar: false,
    });

    const actionSignUp = () => {
        setMessage(null);
        setShowModal(true);
        signUp(email, password)
            .then(() => {
                navigate("/login?signup=success");
            }).catch((error) => {
                setMessage(error);       
            }).finally(() => {
                setShowModal(false);
            });
    }

    useEffect(() => {
        const params = { "email": email, "password": password, "repassword": repassword }
        const result = emptyFieldsSignUp(params);

        setButtonDisabled(!result.buttonDisabled);
        setError(!result.equalPassword)
        setStrength(result.strengthCriteria)
    }, [email, password, repassword]);

    return (
        <div>
            <ModalComponent showModal={showModal} />
            <main className="app-content">
                <Alert variant="danger" hidden={message === null}>{message}</Alert>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control type="email" placeholder="Email"
                            value={email} onChange={(e) => setEmail(e.target.value)}
                            required />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Control type="password" placeholder="Password"
                            value={password} onChange={(e) => setPassword(e.target.value)}
                            required />
                    </Form.Group>

                    <ul style={{ fontSize: "12px" }}>
                        <li style={{ color: strength.minLength ? 'green' : 'red' }}>
                            {Constants.MINIMUM_CHAR}
                        </li>
                        <li style={{ color: strength.hasLowercase ? 'green' : 'red' }}>
                            {Constants.CONTAINS_LOWER_CASE}
                        </li>
                        <li style={{ color: strength.hasUppercase ? 'green' : 'red' }}>
                            {Constants.CONTAINS_UPPER_CASE}
                        </li>
                        <li style={{ color: strength.hasNumber ? 'green' : 'red' }}>
                            {Constants.CONTAINS_NUMBER}
                        </li>
                        <li style={{ color: strength.hasSpecialChar ? 'green' : 'red' }}>
                            {Constants.CONTAINS_SPECIAL_CHAR}
                        </li>
                    </ul>

                    <Form.Group className="mb-3" controlId="formBasicRePassword">
                        <Form.Control type="password" placeholder="Repeate Password"
                            value={repassword} onChange={(e) => setRePassword(e.target.value)}
                            required />
                    </Form.Group>

                    {
                        error && <div>
                            <small style={{ color: "red" }}>password no match</small>
                        </div>
                    }
                    <ButtonToolbar>
                        <ButtonGroup className="me-2">
                            <Button className="button" onClick={actionSignUp} disabled={buttonDisabled}>
                                Save
                            </Button>
                        </ButtonGroup>
                    </ButtonToolbar>
                </Form>
            </main>
        </div>
    )
}

export default SignUp