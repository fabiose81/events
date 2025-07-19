import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Nav from 'react-bootstrap/Nav';
import Alert from 'react-bootstrap/Alert';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ModalComponent from '../components/ModalComponent'
import { login } from '../service/Request'
import { emptyFields } from '../utils/Validade'
import { setMessageState } from '../utils/UIUtils'
import { Constants } from '../utils/Constants'

const Login = () => {

    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [buttonDisabled, setButtonDisabled] = useState(true)
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState({
        label: null,
        variant: null
    });

    useEffect(() => {
        const params = { "email": email, "password": password }
        setButtonDisabled(!emptyFields(params))

        const success = searchParams.get("signup");
        if (success) {
            setMessage(() => setMessageState(Constants.SIGN_UP_SUCCESSFUL, 'success'));
        }

    }, [email, password, searchParams]);

    const actionLogin = () => {
        setShowModal(true);
        login(email, password)
            .then(result => {
                localStorage.setItem('token', result);
                navigate("/event");
            }).catch((error) => {
                setMessage(() => setMessageState(error, 'danger'));
            }).finally(() => {
                setShowModal(false);
            });
    }

    return (
        <div>       
            <ModalComponent data-testid="modal" showModal={showModal} label="logging in"/>
            <main className="app-content">
                 <Alert data-testid="alert" variant={message.variant} hidden={message.label === null}>{message.label}</Alert>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control data-testid="email" type="email" placeholder="Email"
                            value={email} onChange={(e) => setEmail(e.target.value)}
                            required />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Control data-testid="password" type="password" placeholder="Password"
                            value={password} onChange={(e) => setPassword(e.target.value)}
                            required />
                    </Form.Group>
                    <ButtonToolbar>
                        <ButtonGroup className="me-2">
                            <Button data-testid="buttonLogin" className="button" onClick={actionLogin} disabled={buttonDisabled}>Login</Button>
                        </ButtonGroup>
                        <ButtonGroup className="me-2">
                            <Nav.Link href="/sign-up">
                                <Button data-testid="signUp" className="button" variant="success">
                                    Sign Up
                                </Button>
                            </Nav.Link>
                        </ButtonGroup>
                    </ButtonToolbar>
                </Form>
            </main>
        </div>
    )
}

export default Login