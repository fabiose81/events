import { useState, useEffect, useContext } from 'react';
import Main from './Main';
import ListGroup from 'react-bootstrap/ListGroup';
import Alert from 'react-bootstrap/Alert';
import Form from 'react-bootstrap/Form';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';
import ModalComponent from '../components/ModalComponent'
import { getEvents, addEvent, deleteEvent } from '../service/Request'
import { setMessageState } from '../utils/UIUtils'
import { MyContext } from '../utils/MyContext';

const Event = () => {

    const contextValue = useContext(MyContext);
    const [events, setEvents] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [description, setDescription] = useState('');
    const [buttonDisabled, setButtonDisabled] = useState(true)
    const [message, setMessage] = useState({
        label: '',
        variant: ''
    });

    const loadEvents = () => {
        setShowModal(true);
        getEvents()
            .then(result => {
                setEvents(JSON.parse(result));
            }).catch((error) => {
                setMessage(() => setMessageState(error, 'danger'));
            }).finally(() => {
                setShowModal(false);
            });
    }

    const actionAddEvent = () => {
        setShowModal(true);
        parseResponse(addEvent(description))
    }

    const actionDeleteEvent = (event) => {
        setShowModal(true);
        const id = event.target.id
        parseResponse(deleteEvent(id))
    }

    const parseResponse = (event) => {
        event
            .then((response) => {
                setMessage(() => setMessageState(response, 'success'));
                setDescription("");
                setButtonDisabled(true);
                loadEvents();
            }).catch((error) => {
                setMessage(() => setMessageState(error, 'danger'));
            }).finally(() => {
                setShowModal(false);
            });
    }

    useEffect(() => {
        if (contextValue.token) {
            loadEvents();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            <Main>
                <Alert variant={message.variant} hidden={message.label === null}>{message.label}</Alert>
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Control placeholder="Description"
                            value={description} onChange={(e) => {
                                setDescription(e.target.value)
                                const emptyField = e.target.value.trim().length > 0;
                                setButtonDisabled(!emptyField);
                            }
                            }
                            maxLength={100}
                            required />
                    </Form.Group>
                    <ButtonToolbar>
                        <ButtonGroup className="me-2">
                            <Button className="button" onClick={actionAddEvent} disabled={buttonDisabled}>
                                Save
                            </Button>
                        </ButtonGroup>
                    </ButtonToolbar>
                </Form>
                <br />
                <ListGroup as="ol">
                    {
                        events.map((item, index) => (
                            <ListGroup.Item key={index} className="d-flex justify-content-between align-items-start">
                                  <div className="ms-2 me-auto">                                 
                                        {item.description}
                                    </div>
                                    <div>                                 
                                         <Button onClick={actionDeleteEvent} style={{ backgroundColor: "transparent", border: "none" }}>
                                            <Image src="recycle-bin.png" id={item._id.$oid} style={{ width: "32px", height: "32px" }}></Image>
                                        </Button>
                                    </div>
                            </ListGroup.Item>
                        ))
                    }
                </ListGroup>
                <ModalComponent showModal={showModal} />
            </Main>
        </>
    )
}

export default Event